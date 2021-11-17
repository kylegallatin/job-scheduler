from jinja2 import Template
import yaml
from kubernetes import client, config

class JobScheduler:

    def __init__(self):
        pass

    def create(self):
        raise NotImplementedError

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, "r") as f:
            contents = f.read()
        return contents


class K8sJobScheduler(JobScheduler):

    def __init__(self):
        config.load_incluster_config()
        self.client = client.BatchV1Api()
        self.job_template = self.read_file(
            "templates/job.yaml"
        )

    def create_job(self, job_name: str, gcs_path: str, run_command: str) -> bool:
        job_spec = self.render_template(job_name = job_name, gcs_path = gcs_path, run_command = run_command)
        job_spec_yaml = yaml.load(job_spec, Loader=yaml.FullLoader)
        self.client.create_namespaced_job("default", job_spec_yaml, pretty="true")

    def render_template(self, **kwargs) -> str:
        job_spec = Template(self.job_template).render(
            context = self.__dict__,
            job_name = kwargs["job_name"],
            gcs_path = kwargs["gcs_path"],
            run_command = kwargs["run_command"],
            job_meta = kwargs
        )
        return job_spec

    def get_job_status(self, job_name: str) -> dict:
        """
        This returns a dictionary representation of Kubernetes Job Status Object:

        {'active': None,
        'completion_time': datetime.datetime(2021, 11, 12, 15, 13, 18, tzinfo=tzlocal()),
        'conditions': [{'last_probe_time': datetime.datetime(2021, 11, 12, 15, 13, 18, tzinfo=tzlocal()),
                        'last_transition_time': datetime.datetime(2021, 11, 12, 15, 13, 18, tzinfo=tzlocal()),
                        'message': None,
                        'reason': None,
                        'status': 'True',
                        'type': 'Complete'}],
        'failed': None,
        'start_time': datetime.datetime(2021, 11, 12, 15, 12, 44, tzinfo=tzlocal()),
        'succeeded': 1}
        """
        job = self.client.read_namespaced_job(job_name, "default", pretty="true")
        return job.status.to_dict()