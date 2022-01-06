from n_utils.ndt_project import list_jobs
import json


def test_list_jobs():
    jobs = list_jobs(json=True, export_job_properties=True)
    for branch in jobs["branches"]:
        if branch["name"] == "master":
            assert len(branch["components"]) == 1
            assert branch["components"][0]["name"] == "test"
            nametype = {}
            assert len(branch["components"][0]["subcomponents"]) == 5
            for subcomponent in branch["components"][0]["subcomponents"]:
                nametype[subcomponent["name"]] = subcomponent["type"]
            assert nametype["dockertest"] == "docker"
            assert nametype["teststack"] == "stack"
            assert nametype["test"] == "serverless"
