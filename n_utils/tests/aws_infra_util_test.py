from n_utils.aws_infra_util import yaml_to_dict

STACK_PARAMS = {
  "paramEnvId": "dev",
  "BucketArn": "arn:aws:s3:::dev-my-test-bucket",
  "BucketDomainName": "dev-my-test-bucket.s3.amazonaws.com",
  "BucketName": "dev-my-test-bucket",
  "paramDeployToolsVersion": "alpha"
}

def test_merge_import(mocker):
    result = yaml_to_dict('n_utils/tests/templates/test.yaml')
    assert result['Parameters']['paramTest']['Default'] == 'test2'
    assert result['Parameters']['paramTest3']['Default'] == 'test2'
    assert result['Parameters']['paramTest4']['Default'] == 'test2'
    assert result['Parameters']['paramTestA']['Default'] == 'test2'
    assert result['Parameters']['paramTest5']['Default'] == 'TEST2'
    assert result['Parameters']['paramTest6']['Default'] == 'TEST2'
    assert result['Parameters']['paramTest7']['Default'] == 'tEST2'
    assert result['Parameters']['paramTest2']['Default'] == 'TEST2'
    assert result['Parameters']['paramTest8']['Default'] == 'aaabbbST2'
    assert result['Parameters']['paramTest9']['Default'] == 'aabbbST2'
    assert result['Parameters']['paramTest10']['Default'] == 'b/c/d/e/f'
    assert result['Parameters']['paramTest11']['Default'] == 'f'
    assert result['Parameters']['paramTest12']['Default'] == 'a/b/c/d/e'
    assert result['Parameters']['paramTest13']['Default'] == 'a'
    assert result['Parameters']['paramTest14']['Default'] == 'a/b/c/d/e/f'
    assert result['Parameters']['paramTest15']['Default'] == 'b/c/'
    assert result['Parameters']['paramTest16']['Default'] == 'foo'
    assert result['Parameters']['paramTest17']['Default'] == 'foo'
    assert result['Parameters']['paramTest18']['Default'] == 'bar'

def test_just_import(mocker):
    result = yaml_to_dict('n_utils/tests/templates/test-param-import.yaml')
    assert result['Parameters']['paramTest']['Default'] == 'test2'
    assert result['Parameters']['paramTest3']['Default'] == 'test2'
    assert result['Parameters']['paramTest4']['Default'] == 'test2'
    assert result['Parameters']['paramTestA']['Default'] == 'test2'
    assert result['Parameters']['paramTest5']['Default'] == 'TEST2'
    assert result['Parameters']['paramTest6']['Default'] == 'TEST2'
    assert result['Parameters']['paramTest7']['Default'] == 'tEST2'


def test_stackref_order(mocker, stack_params_and_outputs_and_stack):
    stack_params_and_outputs_and_stack.return_value = (STACK_PARAMS, None)
    result = yaml_to_dict('n_utils/tests/templates/test-stackref.yaml')
    assert result["Resources"]["resTaskDefinition"]["Properties"]["ContainerDefinitions"][0]["Environment"][0]["Value"] == \
           "{\n  \"s3\": [{\n    \"path\": \"/${x-forwarded-for}/*\",\n    \"bucket\": \"dev-my-test-bucket\",\n    \"basePath\": \"\",\n    \"region\": \"${AWS::Region}\"\n  }]\n}\n"
    assert result["Resources"]["resBackendRole"]["Properties"]["Policies"][0]["PolicyDocument"]["Statement"][1]["Resource"] == \
           "arn:aws:s3:::dev-my-test-bucket/"
    assert result["Resources"]["resInboxPolicy"]["Properties"]["Bucket"]["Fn::Sub"] == "${myBucket.Arn}/*"