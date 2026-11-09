
import os
import sys
import argparse
import requests

from urllib.parse import quote
from requests.auth import HTTPBasicAuth
from requests.exceptions import RequestException


class JenkinsAPI:
    def __init__(self, url, username, token):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, token)
        self.session.headers.update({
            "Accept": "application/json"
        })
        self.timeout = 15

    def get(self, endpoint):
        """Wysyła zapytanie GET do Jenkins API."""
        response = self.session.get(
            f"{self.url}/{endpoint.lstrip('/')}",
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    def get_crumb(self):
        """Pobiera token CSRF, jeśli Jenkins go wymaga."""
        try:
            response = self.get("crumbIssuer/api/json")
            data = response.json()

            return {
                data["crumbRequestField"]: data["crumb"]
            }
        except requests.HTTPError as error:
            # Brak skonfigurowanego Crumb Issuer (404)
            if error.response is not None and error.response.status_code == 404:
                return {}
            raise

    def post(self, endpoint):
        """Wysyła zapytanie POST, uwzględniając CSRF."""
        headers = self.get_crumb()

        response = self.session.post(
            f"{self.url}/{endpoint.lstrip('/')}",
            headers=headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response

    @staticmethod
    def encode_path(path):
        """Koduje segmenty ścieżki, zachowując separatory folderów."""
        return "/".join(
            quote(part, safe="")
            for part in path.split("/")
        )

    def get_all_jobs(self):
        """Pobiera rekurencyjnie wszystkie zadania Jenkins."""
        jobs = []

        def fetch_folder(folder_path=""):
            endpoint = (
                f"job/{self.encode_path(folder_path)}/"
                if folder_path else ""
            )

            data = self.get(
                f"{endpoint}api/json?tree=jobs[name,fullName,_class]"
            ).json()

            for job in data.get("jobs", []):
                name = job["name"]
                full_name = job.get("fullName", name)
                job_class = job.get("_class", "")

                jobs.append({
                    "name": name,
                    "fullName": full_name,
                    "class": job_class
                })

                # Folder Jenkins może zawierać kolejne zadania
                if "Folder" in job_class or "OrganizationFolder" in job_class:
                    fetch_folder(full_name)

        fetch_folder()
        return jobs

    def get_last_build_status(self, job_name):
        """Sprawdza status ostatniego buildu wybranego zadania."""
        encoded_name = self.encode_path(job_name)

        endpoint = (
            f"job/{encoded_name}/"
            "lastBuild/api/json"
            "?tree=number,result,building,url,timestamp"
        )

        try:
            build = self.get(endpoint).json()

            if build.get("building"):
                status = "BUILDING"
            else:
                status = build.get("result") or "UNKNOWN"

            return {
                "job": job_name,
                "number": build.get("number"),
                "status": status,
                "url": build.get("url")
            }

        except requests.HTTPError as error:
            if error.response is not None and error.response.status_code == 404:
                return {
                    "job": job_name,
                    "number": None,
                    "status": "NO BUILDS",
                    "url": None
                }
            raise

    def run_job(self, job_name):
        """Uruchamia wybrane zadanie Jenkins."""
        encoded_name = self.encode_path(job_name)

        response = self.post(
            f"job/{encoded_name}/build"
        )

        queue_url = response.headers.get("Location")

        return {
            "job": job_name,
            "status": "TRIGGERED",
            "queue_url": queue_url
        }


def main():
    parser = argparse.ArgumentParser(
        description="Jenkins API - zarządzanie zadaniami"
    )

    parser.add_argument(
        "action",
        choices=["list", "status", "run"],
        help="Operacja do wykonania"
    )

    parser.add_argument(
        "--job",
        help="Nazwa zadania (dla status i run)"
    )

    args = parser.parse_args()

    # Konfiguracja pobierana ze zmiennych środowiskowych
    url = os.getenv("JENKINS_URL")
    username = os.getenv("JENKINS_USER")
    token = os.getenv("JENKINS_TOKEN")

    if not all([url, username, token]):
        print("ERROR: Brak konfiguracji Jenkins API.")
        print("Ustaw JENKINS_URL, JENKINS_USER i JENKINS_TOKEN.")
        sys.exit(1)

    if args.action in ("status", "run") and not args.job:
        parser.error("Operacja status/run wymaga parametru --job")

    jenkins = JenkinsAPI(url, username, token)

    try:
        if args.action == "list":
            jobs = jenkins.get_all_jobs()

            print("\n=== LISTA ZADAŃ JENKINS ===")

            for job in jobs:
                print(f"- {job['fullName']}")

            print(f"\nLiczba zadań: {len(jobs)}")

        elif args.action == "status":
            result = jenkins.get_last_build_status(args.job)

            print("\n=== STATUS OSTATNIEGO BUILDU ===")
            print(f"Job:    {result['job']}")
            print(f"Build:  {result['number']}")
            print(f"Status: {result['status']}")
            print(f"URL:    {result['url']}")

        elif args.action == "run":
            result = jenkins.run_job(args.job)

            print("\n=== URUCHOMIENIE ZADANIA ===")
            print(f"Job:    {result['job']}")
            print(f"Status: {result['status']}")
            print(f"Queue:  {result['queue_url']}")

    except requests.HTTPError as error:
        code = error.response.status_code if error.response is not None else "?"
        print(f"HTTP ERROR {code}: {error}")
        if code == 401:
            print("Sprawdź login i API Token.")
        elif code == 403:
            print("Brak uprawnień lub problem z ochroną CSRF.")
        sys.exit(1)

    except RequestException as error:
        print(f"CONNECTION ERROR: {error}")
        sys.exit(1)

    except (ValueError, KeyError) as error:
        print(f"API RESPONSE ERROR: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
