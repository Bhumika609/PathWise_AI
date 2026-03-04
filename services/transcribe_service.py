# services/transcribe_service.py
import os
import time
import uuid
import json
import boto3
import logging
import urllib.request

logger = logging.getLogger("transcribe_service")
logger.setLevel(logging.INFO)

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

transcribe = boto3.client("transcribe", region_name=AWS_REGION)

def start_transcription_job(s3_uri: str, media_format: str = "mp3", language_code: str = "en-IN") -> str:
    """
    Starts an AWS Transcribe job and returns the job name.
    """
    job_name = f"pathwise-{uuid.uuid4().hex}"

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=media_format,
        Media={"MediaFileUri": s3_uri},
        Settings={
            "ShowSpeakerLabels": False,
            "ShowAlternatives": False
        }
    )

    logger.info(f"Started Transcribe job: {job_name}")
    return job_name


def wait_for_transcription(job_name: str, timeout_seconds: int = 120) -> dict:
    """
    Polls until job completes or fails. Returns the final job response.
    """
    start = time.time()

    while True:
        resp = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        status = resp["TranscriptionJob"]["TranscriptionJobStatus"]

        if status in ("COMPLETED", "FAILED"):
            return resp

        if time.time() - start > timeout_seconds:
            raise TimeoutError(f"Transcribe job timed out after {timeout_seconds}s: {job_name}")

        time.sleep(2)


def fetch_transcript_text(transcript_file_uri: str) -> str:
    """
    Downloads the Transcribe JSON result and returns transcript text.
    """
    with urllib.request.urlopen(transcript_file_uri) as r:
        data = json.loads(r.read().decode("utf-8"))

    # Standard Transcribe format
    return data["results"]["transcripts"][0]["transcript"]
