import shutil
import subprocess
import json
from typing import Tuple
from .base import BaseVowHandler


class CloudVowHandlers(BaseVowHandler):
    """
    =============================================================================
    == THE CELESTIAL DIPLOMAT (V-Ω-INFRASTRUCTURE-AWARE)                       ==
    =============================================================================
    Judges the configuration of Cloud CLI tools to prevent catastrophic deployments.
    """

    def _vow_aws_identity_loaded(self) -> Tuple[bool, str]:
        """Asserts that AWS credentials are loaded and valid."""
        if not shutil.which("aws"): return False, "AWS CLI missing."
        try:
            subprocess.run(
                ["aws", "sts", "get-caller-identity"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True
            )
            return True, "AWS Identity confirmed."
        except:
            return False, "AWS Identity unverifiable (Check credentials)."

    def _vow_aws_region_is(self, region: str) -> Tuple[bool, str]:
        """Asserts the active AWS region matches the requirement."""
        try:
            res = subprocess.run(["aws", "configure", "get", "region"], capture_output=True, text=True)
            current = res.stdout.strip()
            return current == region, f"AWS Region is '{current}' (Expected '{region}')."
        except:
            return False, "Could not determine AWS Region."

    def _vow_k8s_context_is(self, allowed_context_regex: str) -> Tuple[bool, str]:
        """
        [THE PRODUCTION GUARD]
        Asserts the current Kubernetes context matches a pattern.
        Usage: `?? k8s_context_is: minikube|staging`
        """
        import re
        if not shutil.which("kubectl"): return False, "Kubectl missing."
        try:
            res = subprocess.run(["kubectl", "config", "current-context"], capture_output=True, text=True)
            current = res.stdout.strip()
            if re.match(allowed_context_regex, current):
                return True, f"K8s context '{current}' is allowed."
            return False, f"DANGER: K8s context '{current}' does not match '{allowed_context_regex}'."
        except:
            return False, "Could not determine K8s context."

    def _vow_terraform_initialized(self, path: str) -> Tuple[bool, str]:
        """Asserts a Terraform directory has been initialized (.terraform exists)."""
        target = self._resolve(path) / ".terraform"
        return target.is_dir(), "Terraform initialized." if target.is_dir() else "Terraform not initialized."

    def _vow_git_branch_is_protected(self, protection_regex: str = "main|master|prod") -> Tuple[bool, str]:
        """
        [THE RELEASE SENTINEL]
        Asserts the current branch matches a protected pattern.
        Useful for 'release' symphonies that should only run on main.
        """
        import re
        try:
            res = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True,
                                 cwd=self.root)
            current = res.stdout.strip()
            if re.match(protection_regex, current):
                return True, f"Branch '{current}' is protected."
            return False, f"Branch '{current}' is NOT protected."
        except:
            return False, "Not a git repository."
