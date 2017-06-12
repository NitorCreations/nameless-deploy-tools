public class Settings {
    public final gitUrl
    public final gitCredentials
    private final workspace
	private final jobPropertiesDir
    private final Map propFiles = [:]
    private final Map jobTriggers = [:]
    private final Map stackImageMap = [:]
    public Settings(remoteConfig, __FILE__) {
        this.gitUrl = remoteConfig.url
        this.gitCredentials = remoteConfig.credentialsId
        this.workspace = new File(__FILE__).parentFile.absoluteFile
        this.jobPropertiesDir = new File(workspace, "job-properties")
        
        def jobDefs = getJobs()
        /**
         * Get mappings for image jobs to trigger (and block) deploy jobs
         **/
        for (jobDef in jobDefs) {
            def ( imageDir, gitBranch, jobType, stackName ) = jobDef.tokenize(':')
            if ("stack" == jobType) {
                def imageJobName = getJobName(gitBranch, imageDir)
                def jobName = getJobName(gitBranch, imageDir, stackName)
                if (imageJobName != null) {
                    stackImageMap["$gitBranch-$imageDir-$stackName"] = imageJobName
                }
                def properties = loadStackProps(gitBranch, imageDir, stackName)
                def jobPrefix = properties.JENKINS_JOB_PREFIX
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
        /*
        def ret = []
        ret << "centos-jenkins:dev:image:-"
        ret << "centos-jenkins:dev:stack:amibakery"
        ret << "centos-jenkins:dev:stack:jenkins"
        ret << "centos-jenkins:master:image:-"
        ret << "centos-jenkins:master:stack:amibakery"
        ret << "centos-jenkins:master:stack:jenkins"
        return ret
        */
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
        return ret
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
            /*
            if (fileName.indexOf("dev") > 0) {
            	properties.JENKINS_JOB_PREFIX = "awsdev"
            } else {
            	properties.JENKINS_JOB_PREFIX = "aws"
            }
            properties.BAKE_IMAGE_BRANCH = "dev"
            properties.AUTOPROMOTE_TO_BRANCH = "master"
            */
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
    public String getJobName(gitBranch, imageDir, stackName="-") {
        def fileName = "${gitBranch}-${imageDir}"
        if (stackName == null || stackName == "-") {
            fileName = "image-${fileName}.properties"
        } else {
            fileName = "stack-${fileName}-${stackName}.properties"
        }
        def properties = loadProps(fileName, true)
        if (properties.JENKINS_JOB_NAME != null) {
            return properties.JENKINS_JOB_NAME
        } else {
            if (properties.JENKINS_JOB_PREFIX == null) {
                return null
            }
        	def jobPrefix = properties.JENKINS_JOB_PREFIX
            if (stackName != null && stackName != "-") { 
            	return "$jobPrefix-$imageDir-deploy-$stackName"
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
/*
def remoteConfig = [:]
remoteConfig.url = "github.com/foo/bar.git"
remoteConfig.credentialsId = "bob-jenkins"
def __FILE__ = './script.groovy'
*/
final Settings s = new Settings(remoteConfig, __FILE__)

def private addSCMTriggers(job, properties, s) {
    job.with {
        triggers {
            if (properties.STACK_CRON != null) {
                cron(properties.IMAGE_CRON)
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
    def jobPrefix = imageProperties.JENKINS_JOB_PREFIX
    def jobName = s.getJobName(gitBranch, imageDir, stackName) 
    if (jobName == null) {
        continue
    }
    //def blockOnArray = [SEED_JOB.name]
    def blockOnArray = ["generate-jobs"]
    if (jobType == "stack") {
        properties = s.loadStackProps(gitBranch, imageDir, stackName)
        jobPrefix = properties.JENKINS_JOB_PREFIX
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
        def job = pipelineJob(jobName) {
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
                 excludedRegions: '\\\\Q$imageDir/stack-$stackName/\\\\E.*',
                 includedRegions: '\\\\Q$imageDir/image/\\\\E.*']],
              submoduleCfg: [],
              userRemoteConfigs: [[credentialsId: \"$s.gitCredentials\",
              url: \"$s.gitUrl\"]]])
    wrap([\$class: 'AnsiColorBuildWrapper']) {
        ${dryRun}stage \"Deploy or update stack\"
        sh \"ndt deploy-stack $imageDir $stackName \\\"\$AMI_ID\\\" $imageTag\"
    }
}
""")
                }
            }
            description("nitor-deploy-tools deploy stack job")
            blockOn(blockOnArray)
            publishers {
                archiveArtifacts("ami.properties")
            }
        }
        addSCMTriggers(job, properties, s)
        if (viewMap[jobPrefix] == null) {
            viewMap[jobPrefix] = [jobName]
        } else {
            viewMap[jobPrefix] << jobName
        }
        if (properties.AUTOPROMOTE_TO_BRANCH != null) {
            targetJobs = []
            for (toBranch in properties.AUTOPROMOTE_TO_BRANCH.split(",")) {
                if (toBranch != gitBranch) {
                	targetJobs << s.getJobName(toBranch, imageDir)
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
                description("nitor-deploy-tools undeploy stack job")
                blockOn([jobName])
            }
            viewMap[jobPrefix] << undeployJobName
        }
    } else {
        properties = imageProperties
        if ("y" == properties.SKIP_IMAGE_JOB || (imageDir == "bootstrap" && "n" != properties.SKIP_IMAGE_JOB)) {
            continue
        }
        jobPrefix = properties.JENKINS_JOB_PREFIX
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
        if (properties.BAKE_IMAGE_BRANCH != null && properties.BAKE_IMAGE_BRANCH != gitBranch) {
            /**
             * Create a image promotion job instead of a image baking job
             **/
            println "Generating image promote job $jobName"
            promotableJob = s.getJobName(properties.BAKE_IMAGE_BRANCH, imageDir)
            job.with {
                steps {
                    shell("ndt bake-image " + imageDir)
                }
                description("nitor-deploy-tools promote image job")
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
println it
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
                description("nitor-deploy-tools bake image job")
                configure { project ->
                    project / 'scm' / 'extensions' << 'hudson.plugins.git.extensions.impl.PathRestriction' {
                        includedRegions "\\Q$imageDir/image/\\E.*"
                        excludedRegions ""
                    }
                    project / 'buildWrappers' << 'hudson.plugins.ansicolor.AnsiColorBuildWrapper' {
                        colorMapName 'xterm'
                    }
                }
            }
        }
        addSCMTriggers(job, properties, s)
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
