public class Settings {
    public final gitUrl
    public final gitCredentials
    private final workspace
    private final jobPropertiesDir
    private final Map propFiles = [:]
    private final Map jobTriggers = [:]
    private final Map stackImageMap = [:]
    private jobDefs = null
    public Settings(remoteConfig, __FILE__) {
        this.gitUrl = remoteConfig.url
        this.gitCredentials = remoteConfig.credentialsId
        this.workspace = new File(__FILE__).parentFile.absoluteFile
        this.jobPropertiesDir = new File(workspace, "job-properties")
        
        /**
         * Get mappings for image jobs to trigger (and block) deploy jobs
         **/
        for (jobDef in this.getJobs()) {
            def ( imageDir, gitBranch, jobType, stackName ) = jobDef.tokenize(':')
            if ("stack" == jobType) {
                def imageJobName = this.getJobName(gitBranch, imageDir, "image", "-")
                def jobName = this.getJobName(gitBranch, imageDir, jobType, stackName)
                if (imageJobName != null) {
                    stackImageMap["$gitBranch-$imageDir-$stackName"] = imageJobName
                }
                def properties = loadStackProps(gitBranch, imageDir, stackName)
                def jobPrefix = properties.BUILD_JOB_PREFIX
                if ("y" != properties.MANUAL_DEPLOY) {
                    if (jobTriggers["$gitBranch-$imageDir"] == null) {
                        jobTriggers["$gitBranch-$imageDir"] = [jobName]
                    } else {
                        jobTriggers["$gitBranch-$imageDir"] << jobName
                    }
                }
            }
        }
    }
    /**
     * Runs `ndt list-jobs` and returns the result as a string array
     **/
    public String[] getJobs() {
        if (this.jobDefs == null) {
            def process = new ProcessBuilder(["ndt", "list-jobs"])
                    .redirectErrorStream(true)
                    .directory(this.workspace)
                    .start()
            def ret = []
            process.inputStream.eachLine {
                println it
                ret << it
            }
            process.waitFor();
            this.jobDefs = ret;
        }
        return this.jobDefs
    }
    /**
    * Loads of file into a properties object optionally ignoring FileNotFoundException
    **/
    public Properties loadProps(fileName, quiet=false) {
        if (this.propFiles[fileName] != null) {
            return this.propFiles[fileName]
        } else {
            def properties = new Properties()
            this.propFiles[fileName] = properties
            File propertiesF = new File(this.jobPropertiesDir, fileName)
            try {
                propertiesF.withInputStream {
                    properties.load(it)
                }
            } catch (java.io.FileNotFoundException ex) {
                if (!quiet) {
                    println "Job properties " + propertiesF.absolutePath + " not found"
                }
            } finally {
                return properties
            } 
        }
    }
    /**
     * Load properties for an image job
     */
    public Properties loadImageProps(gitBranch, imageDir, quiet=false) {
        return loadProps("image-$gitBranch-${imageDir}.properties", quiet)
    }
    /**
     * Load properties for a deploy job
     **/
    public Properties loadStackProps(gitBranch, imageDir, stackName, quiet=false) {
        return loadProps("stack-$gitBranch-$imageDir-${stackName}.properties", quiet)
    }
    /**
     * Load properties for a docker job
     **/
    public Properties loadDockerProps(gitBranch, imageDir, dockerName, quiet=false) {
        return loadProps("docker-$gitBranch-$imageDir-${dockerName}.properties", quiet)
    }
    /**
     * Gets triggers defined for a bake job
     **/
    public List getJobTriggers(gitBranch, imageDir) {
        return jobTriggers["$gitBranch-$imageDir"]
    }
    /**
     * Get image job name that matches the stack job
     **/
    public String getImageJobForStack(gitBranch, imageDir, stackName) {
        return stackImageMap["$gitBranch-$imageDir-$stackName"]
    }
    /**
     * Resolves a name for the given job
     **/
    public String getJobName(gitBranch, imageDir, jobType, stackName) {
        def fileName = "${gitBranch}-${imageDir}"
        if (jobType == "image") {
            fileName = "image-${fileName}.properties"
        } else if (jobType == "stack"){
            fileName = "stack-${fileName}-${stackName}.properties"
        } else if (jobType == "docker") {
            fileName = "docker-${fileName}-${stackName}.properties"
        } else {
            return null
        }
        def properties = loadProps(fileName, true)
        if (properties.JENKINS_JOB_NAME != null) {
            return properties.JENKINS_JOB_NAME
        } else {
            if (properties.BUILD_JOB_PREFIX == null) {
                return null
            }
            def jobPrefix = properties.BUILD_JOB_PREFIX
            if (stackName != null && stackName != "-") {
                if (jobType == "stack") {
                    return "$jobPrefix-$imageDir-deploy-$stackName"
                } else if (jobType == "docker") {
                    return "$jobPrefix-$imageDir-docker-bake-$stackName"
                }
            } else if (properties.BAKE_IMAGE_BRANCH != null && properties.BAKE_IMAGE_BRANCH != gitBranch) {
                return "$jobPrefix-$imageDir-promote"
            } else {
                return "$jobPrefix-$imageDir-bake"
            }
        }
    }
    static {
    }
}
remoteConfig = SEED_JOB.scm.userRemoteConfigs[0]
final Settings s = new Settings(remoteConfig, __FILE__)

def private addSCMTriggers(job, jobType, properties, s) {
    if (properties.MANUAL_DEPLOY == "y") {
        return;
    }
    job.with {
        triggers {
            if (jobType == "image" && properties.IMAGE_CRON != null) {
                cron(properties.IMAGE_CRON)
            }
            if (jobType == "stack" && properties.STACK_CRON != null) {
                cron(properties.STACK_CRON)
            }
            if (jobType == "docker" && properties.DOCKER_CRON != null) {
                cron(properties.DOCKER_CRON)
            }
            if (s.gitUrl.indexOf("github.com") > -1) {
                githubPush()
            } else if (s.gitUrl.indexOf("bitbucket.org") > -1) {
                bitbucketPush()
            } else if (s.gitUrl.indexOf("gitlab.com") > -1) {
                gitlabPush {
                    buildOnPushEvents(true)
                }
            } else {
                scm('H/5 * * * *')
            }
        }
    }
}
def private addParamTriggers(job, gitBranch, imageDir, s) {
    if (s.getJobTriggers(gitBranch, imageDir) != null) {
        job.with {
            publishers {
                downstreamParameterized {
                    trigger(s.getJobTriggers(gitBranch, imageDir)) {
                        condition('SUCCESS')
                        parameters {
                            propertiesFile("ami.properties")
                        }
                    }
                }
            }
        }
    }
}
viewMap = [:]
jobDefs = s.getJobs()
/**
 * Do the actual job generation
 **/
for (jobDef in jobDefs) {
    def ( imageDir, gitBranch, jobType, stackName ) = jobDef.tokenize(':')
    Properties properties
    Properties imageProperties = s.loadImageProps(gitBranch, imageDir, true)
    def jobPrefix = imageProperties.BUILD_JOB_PREFIX
    def jobName = s.getJobName(gitBranch, imageDir, jobType, stackName)
    if (jobName == null) {
        continue
    }
    def blockOnArray = [SEED_JOB.name]
    if (jobType == "stack") {
        properties = s.loadStackProps(gitBranch, imageDir, stackName)
        jobPrefix = properties.BUILD_JOB_PREFIX
        if ("y" == properties.SKIP_STACK_JOB || (imageDir == "bootstrap" && "n" != properties.SKIP_STACK_JOB)) {
            continue
        }
        println "Generating stack deploy job $jobName"
        imageJob = s.getImageJobForStack(gitBranch, imageDir, stackName)
        if (imageJob != null) {
            imageTag = imageJob.replaceAll("-", "_")
            blockOnArray << imageJob
        } else {
            imageTag = ""
        }
        def dryRun = ""
        if ((gitBranch == "prod" && "n" != properties.MANUAL_ACCEPT_DEPLOY) ||
            "y" == properties.MANUAL_ACCEPT_DEPLOY) {
           dryRun = "stage \"Dry run to accept changeset\"\n" +
                    "        sh \"ndt deploy-stack -d $imageDir $stackName \\\"\$AMI_ID\\\" $imageTag\"\n" +
                    "        input(message: \"Does the changeset above look ok?\")\n        "
        }
        def postDeploy=""
        if (properties.POST_DEPLOY != null) {
            postDeploy="sh \"" + properties.POST_DEPLOY + "\""
        }
        def job = pipelineJob(jobName) {
            parameters {
                stringParam('AMI_ID', '', 'Ami id if triggered from a bake job')
            }
            definition {
                cps{
                    script("""env.GIT_BRANCH=\"$gitBranch\"
node {
    checkout([\$class: 'GitSCM', branches: [[name: \"*/$gitBranch\"]], 
              doGenerateSubmoduleConfigurations: false,
              extensions: [
                [\$class: 'PathRestriction',
                 includedRegions: '\\\\Q$imageDir/stack-$stackName/\\\\E.*',
                 excludedRegions: '']],
              submoduleCfg: [],
              userRemoteConfigs: [[credentialsId: \"$s.gitCredentials\",
              url: \"$s.gitUrl\"]]])
    wrap([\$class: 'AnsiColorBuildWrapper']) {
        ${dryRun}stage \"Deploy or update stack\"
        sh \"ndt deploy-stack $imageDir $stackName \\\"\$AMI_ID\\\" $imageTag\"
        ${postDeploy}
    }
    archiveArtifacts artifacts: 'ami.properties'
}
""")
                }
            }
            description("nameless-deploy-tools deploy stack job")
            blockOn(blockOnArray)
        }
        addSCMTriggers(job, jobType, properties, s)
        if (viewMap[jobPrefix] == null) {
            viewMap[jobPrefix] = [jobName]
        } else {
            viewMap[jobPrefix] << jobName
        }
        if (properties.AUTOPROMOTE_TO_BRANCH != null) {
            targetJobs = []
            for (toBranch in properties.AUTOPROMOTE_TO_BRANCH.split(",")) {
                if (toBranch != gitBranch) {
                    targetJobs << s.getJobName(toBranch, imageDir, "image", "-")
                }
            }
            job.with {
                publishers {
                    downstreamParameterized {
                        trigger(targetJobs) {
                            condition('SUCCESS')
                            parameters {
                                propertiesFile("ami.properties")
                            }
                        }
                    }
                }
            }
        }
        if ("y" != properties.DISABLE_RAMPDOWN) {
            def undeployJobName = jobName.replaceAll("deploy", "undeploy")
            if (undeployJobName == jobName) {
                undeployJobName += "-undeploy"
            }
            def undeployJob = freeStyleJob(undeployJobName) {
                parameters {
                    choiceParam('CONFIRM', ["No", "Yes"], 'Are you sure?')
                }
                scm {
                    git {
                        remote {
                            name("origin")
                            url(s.gitUrl)
                            credentials(s.gitCredentials)
                        }
                        branch(gitBranch)
                    }
                }
                steps {
                    shell("""if ! [ \"Yes\" = \"\$CONFIRM\" ]; then
  exit 1
fi
ndt undeploy-stack $imageDir $stackName
""")
                }
                description("nameless-deploy-tools undeploy stack job")
                blockOn([jobName])
            }
            viewMap[jobPrefix] << undeployJobName
        }
    } else if (jobType == "docker") {
        properties = s.loadDockerProps(gitBranch, imageDir, stackName)
        jobPrefix = properties.BUILD_JOB_PREFIX
        if ("y" == properties.SKIP_DOCKER_JOB || (imageDir == "bootstrap" && "n" != properties.SKIP_DOCKER_JOB)) {
            continue
        }
        if (properties.BAKE_IMAGE_BRANCH != null && properties.BAKE_IMAGE_BRANCH != gitBranch) {
            continue
        }
        println "Generating docker bake job $jobName"
        def job = freeStyleJob(jobName) {
            scm {
                git {
                    remote {
                        name("origin")
                        url(s.gitUrl)
                        credentials(s.gitCredentials)
                    }
                    branch(gitBranch)
                }
            }
            blockOn(blockOnArray)
        }
        addSCMTriggers(job, jobType, properties, s)
        job.with {
            steps {
                shell("ndt bake-docker " + imageDir + " " + stackName)
            }
            description("nameless-deploy-tools bake docker job")
            configure { project ->
                project / 'scm' / 'extensions' << 'hudson.plugins.git.extensions.impl.PathRestriction' {
                    includedRegions "\\Q$imageDir/docker-\\E.*"
                }
                project / 'buildWrappers' << 'hudson.plugins.ansicolor.AnsiColorBuildWrapper' {
                    colorMapName 'xterm'
                }
            }
        }
        if (viewMap[jobPrefix] == null) {
            viewMap[jobPrefix] = [jobName]
        } else {
            viewMap[jobPrefix] << jobName
        }
    } else if (jobType == "image") {
        properties = imageProperties
        if ("y" == properties.SKIP_IMAGE_JOB || (imageDir == "bootstrap" && "n" != properties.SKIP_IMAGE_JOB)) {
            continue
        }
        jobPrefix = properties.BUILD_JOB_PREFIX
        def job = freeStyleJob(jobName) {
            scm {
                git {
                    remote {
                        name("origin")
                        url(s.gitUrl)
                        credentials(s.gitCredentials)
                    }
                    branch(gitBranch)
                }
            }
            blockOn(blockOnArray)
        }
        job.with {
            configure { project ->
                project / 'scm' / 'extensions' << 'hudson.plugins.git.extensions.impl.PathRestriction' {
                    includedRegions "\\Q$imageDir/\\E.*"
                    excludedRegions "\\Q$imageDir/stack-\\E.*\n\\Q$imageDir/docker-\\E.*"
                }
                project / 'buildWrappers' << 'hudson.plugins.ansicolor.AnsiColorBuildWrapper' {
                    colorMapName 'xterm'
                }
            }
        }
        if (properties.BAKE_IMAGE_BRANCH != null && properties.BAKE_IMAGE_BRANCH != gitBranch) {
            /**
             * Create a image promotion job instead of a image baking job
             **/
            def promotableJob = s.getJobName(properties.BAKE_IMAGE_BRANCH, imageDir, "image", "-")
            println "Generating image promote job $jobName from $promotableJob"
            job.with {
                steps {
                    shell("ndt promote-image \$AMI_ID $jobName")
                }
                description("nameless-deploy-tools promote image job")
                configure { project ->
                    project / 'properties' / 'hudson.model.ParametersDefinitionProperty' / 'parameterDefinitions' << 'jp.ikedam.jenkins.plugins.extensible__choice__parameter.ExtensibleChoiceParameterDefinition' {
                        name 'AMI_ID'
                        editable 'false'
                        choiceListProvider(class: "jp.ikedam.jenkins.plugins.extensible_choice_parameter.SystemGroovyChoiceListProvider") {
                            groovyScript {
                                script """def process = new ProcessBuilder(["ndt", "get-images", "$promotableJob"])
.redirectErrorStream(true)
.start()
def ret = []
process.inputStream.eachLine {
  ret << it
}
process.waitFor();
return ret
"""
                                sandbox "false"
                            }
                            usePredefinedVariables "false"
                        }
                    }
                }
            }
        } else {
            println "Generating image bake job $jobName"
            job.with {
                steps {
                    shell("ndt bake-image " + imageDir)
                }
                description("nameless-deploy-tools bake image job")
            }
        }
        addSCMTriggers(job, jobType, properties, s)
        addParamTriggers(job, gitBranch, imageDir, s)
        if (viewMap[jobPrefix] == null) {
            viewMap[jobPrefix] = [jobName]
        } else {
            viewMap[jobPrefix] << jobName
        }
    }
}
/**
 * Genereate views for all the jobs
 **/
for (item in viewMap) {
    println item
    listView(item.key) {
        columns {
            status()
            buildButton()
            name()
            progressBar()
            cronTrigger()
            lastBuildConsole()
            lastSuccess()
            lastDuration()
            lastFailure()
        }
        jobs {
            for (jobName in item.value) {
                name(jobName)
            }
        }
    }
}
