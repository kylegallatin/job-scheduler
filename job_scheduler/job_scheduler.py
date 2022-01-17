from jinja2 import Template
import yaml
from kubernetes import client, config


class JobScheduler:

    def __init__(self):
        pass

    def create(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @staticmethod
    def read_file(path: str) -> str:
        with open(path, "r") as f:
            contents = f.read()
        return contents

    @staticmethod
    def preprocess_gcs_path(path: str) -> str:
        return path.strip("/")


class K8sJobScheduler(JobScheduler):

    def __init__(self):
        try:
            config.load_incluster_config()
            self.pod_client = client.CoreV1Api()
            self.job_client = client.BatchV1Api()
        except Exception as e:
            print("Running in debug mode")

        self.job_template = self.read_file("templates/job.yaml")

    def create_job(
        self, job_name: str, gcs_path: str, run_command: str
    ) -> dict:
        job_spec = self.render_template(
            job_name=job_name, gcs_path=gcs_path, run_command=run_command
        )
        job_spec_yaml = yaml.load(job_spec, Loader=yaml.FullLoader)

        job = self.job_client.create_namespaced_job(
            namespace="default", body=job_spec_yaml, pretty="true"
        )
        return job.to_dict()

    def delete_job(self, job_name: str) -> dict:

        status = self.job_client.delete_namespaced_job(
            namespace="default", name=job_name, pretty="true"
        )
        return status.to_dict()

    def render_template(self, **kwargs) -> str:
        job_spec = Template(self.job_template).render(
            context=self.__dict__,
            job_name=kwargs["job_name"],
            gcs_path=self.preprocess_gcs_path(kwargs["gcs_path"]),
            run_command=kwargs["run_command"],
            job_meta=kwargs
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
        job = self.job_client.read_namespaced_job(
            job_name, "default", pretty="true"
        )
        return job.status.to_dict()

    def get_pod_status(self, job_name: str) -> dict:
        """
        Pod status returns significantly more info than job status.
        The 'phase' is likely the most useful metric, though much more info can be derived.
        Common phases: Pending | ContainerCreating | Running | Completed | Error | ImagePullBackOff | CrashLoopBackOff

        Example value:
        {'conditions': [{'last_probe_time': None,
                        'last_transition_time': datetime.datetime(2021, 11, 24, 15, 24, 12, tzinfo=tzlocal()),
                        'message': None,
                        'reason': 'PodCompleted',
                        'status': 'True',
                        'type': 'Initialized'},
                        {'last_probe_time': None,
                        'last_transition_time': datetime.datetime(2021, 11, 24, 15, 24, 39, tzinfo=tzlocal()),
                        'message': None,
                        'reason': 'PodCompleted',
                        'status': 'False',
                        'type': 'Ready'},
                        {'last_probe_time': None,
                        'last_transition_time': datetime.datetime(2021, 11, 24, 15, 24, 39, tzinfo=tzlocal()),
                        'message': None,
                        'reason': 'PodCompleted',
                        'status': 'False',
                        'type': 'ContainersReady'},
                        {'last_probe_time': None,
                        'last_transition_time': datetime.datetime(2021, 11, 24, 15, 24, 12, tzinfo=tzlocal()),
                        'message': None,
                        'reason': None,
                        'status': 'True',
                        'type': 'PodScheduled'}],
        'container_statuses': [{'container_id': 'docker://98b917cfe253f18e5849e098d7dce539d117c88b8eb34037df55c3d9a10a9e46',
                                'image': 'gcr.io/serene-radius-314018/python/python-base:0.0.2',
                                'image_id': 'docker://sha256:a328356d854e6322671049a0fa010643aa4da747087454b92a64c763aee6953f',
                                'last_state': {'running': None,
                                                'terminated': None,
                                                'waiting': None},
                                'name': 'test',
                                'ready': False,
                                'restart_count': 0,
                                'started': False,
                                'state': {'running': None,
                                        'terminated': {'container_id': 'docker://98b917cfe253f18e5849e098d7dce539d117c88b8eb34037df55c3d9a10a9e46',
                                                        'exit_code': 0,
                                                        'finished_at': datetime.datetime(2021, 11, 24, 15, 24, 38, tzinfo=tzlocal()),
                                                        'message': None,
                                                        'reason': 'Completed',
                                                        'signal': None,
                                                        'started_at': datetime.datetime(2021, 11, 24, 15, 24, 15, tzinfo=tzlocal())},
                                        'waiting': None}}],
        'ephemeral_container_statuses': None,
        'host_ip': '192.168.65.4',
        'init_container_statuses': None,
        'message': None,
        'nominated_node_name': None,
        'phase': 'Succeeded',
        'pod_i_ps': [{'ip': '10.1.0.31'}],
        'pod_ip': '10.1.0.31',
        'qos_class': 'Burstable',
        'reason': None,
        'start_time': datetime.datetime(2021, 11, 24, 15, 24, 12, tzinfo=tzlocal())}
        """
        pod_list = self.pod_client.list_namespaced_pod(
            namespace="default", label_selector=f"job-name={job_name}"
        )
        pod = pod_list.items[0]
        return pod.status.to_dict()

    def get_logs(self, job_name: str) -> str:
        pod_list = self.pod_client.list_namespaced_pod(
            namespace="default", label_selector=f"job-name={job_name}"
        )
        pod_name = pod_list.items[0].metadata.name
        return self.pod_client.read_namespaced_pod_log(
            name=pod_name, namespace='default'
        )
