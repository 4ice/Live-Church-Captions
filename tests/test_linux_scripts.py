from pathlib import Path
import unittest


class LinuxScriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.packages = Path("scripts/linux-system-packages.sh").read_text(encoding="utf-8")
        cls.setup = Path("setup-linux.sh").read_text(encoding="utf-8")
        cls.start = Path("start-linux.sh").read_text(encoding="utf-8")
        cls.cuda_installer = Path("install-cuda-runtime-linux.sh").read_text(encoding="utf-8")
        cls.cuda_helper = Path("scripts/linux-cuda-runtime.sh").read_text(encoding="utf-8")

    def test_common_package_managers_are_detected(self):
        for manager in ("dnf", "apt-get", "zypper", "pacman", "apk", "yum"):
            self.assertIn(manager, self.packages)

    def test_active_linux_firewall_managers_are_detected(self):
        self.assertIn("linux_active_firewall_manager", self.packages)
        self.assertIn("firewall-cmd", self.packages)
        self.assertIn("ufw", self.packages)

    def test_python_floor_is_checked(self):
        self.assertIn("sys.version_info >= (3, 10)", self.packages)
        self.assertIn("find_supported_linux_python", self.setup)

    def test_python_packages_stay_in_virtual_environment(self):
        self.assertIn(".venv/bin/python", self.setup)
        self.assertIn('"$VENV_PY" -m pip install -r requirements.txt', self.setup)

    def test_linux_start_uses_dual_port_runner(self):
        self.assertIn('exec "$VENV_PY" scripts/run-dual.py', self.start)

    def test_linux_cuda_runtime_is_optional_and_project_local(self):
        self.assertIn("install-cuda-runtime-linux.sh", self.setup)
        self.assertIn("status.nvidia_smi_available or status.cuda_device_count > 0", self.setup)
        self.assertIn("Install the local CUDA runtime libraries inside .venv now? [y/N]", self.setup)
        self.assertIn('case "${cuda_answer:-no}"', self.setup)
        self.assertIn("y|Y|yes|YES) ./install-cuda-runtime-linux.sh", self.setup)
        self.assertIn("nvidia-cublas-cu12", self.cuda_installer)
        self.assertIn('"nvidia-cudnn-cu12==9.*"', self.cuda_installer)
        self.assertIn("--force-reinstall --no-cache-dir", self.cuda_installer)
        self.assertIn('prepare_linux_python_cuda_library_path "$VENV_PY"', self.start)
        self.assertIn("nvidia.cublas.lib", self.cuda_helper)
        self.assertIn("nvidia.cudnn.lib", self.cuda_helper)

    def test_linux_setup_offers_least_privilege_audience_firewall_rule(self):
        self.assertIn("Checking recommended audience firewall access", self.setup)
        self.assertIn("Add the recommended audience firewall rule now? [y/N]", self.setup)
        self.assertIn('case "${firewall_answer:-no}"', self.setup)
        self.assertIn("allow_linux_audience_port", self.setup)
        self.assertIn('run_as_root firewall-cmd --permanent --zone="$zone" --add-port="${port}/tcp"', self.packages)
        self.assertIn('run_as_root ufw allow "${port}/tcp"', self.packages)
        self.assertIn("It does not open operator port 9090", self.setup)
        self.assertNotIn('add-port="9090/tcp"', self.packages)


if __name__ == "__main__":
    unittest.main()
