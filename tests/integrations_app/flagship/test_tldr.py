import os

from integrations_app.flagship import _PATH_INTEGRATIONS_DIR

from lightning.app.testing.testing import run_app_in_cloud


def test_app_in_cloud():

    with open(os.path.join(_PATH_INTEGRATIONS_DIR, "test_app.py"), "w") as f:
        app_string = """
        import lightning
        from tests.test_app import DummyTLDR
        app = lightning.app.LightningApp(
            MultiNodeLightningTrainerWithTensorboard(
                DummyTLDR, num_nodes=2, cloud_compute=lightning.CloudCompute("gpu-fast-multi", disk_size=50),
            )
        )
        """
        f.write(app_string)

        with run_app_in_cloud(_PATH_INTEGRATIONS_DIR, "test_app.py") as (_, _, fetch_logs, _):
            logs = list(fetch_logs())

        # for curr_str in expected_strings:
        #     assert curr_str in logs
        print(logs)