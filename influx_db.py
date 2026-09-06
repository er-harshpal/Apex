"""InfluxDB storage layer for Smart Helmet telemetry."""

from __future__ import annotations

import os
from typing import Optional

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBWriter:
    """Handles writing processed helmet telemetry to InfluxDB."""

    def __init__(
        self,
        url: Optional[str] = None,
        token: Optional[str] = None,
        org: Optional[str] = None,
        bucket: Optional[str] = None,
    ) -> None:

        self.url = url or os.getenv("INFLUXDB_URL", "http://localhost:8086")
        self.token = token or os.getenv("INFLUXDB_TOKEN")
        self.org = org or os.getenv("INFLUXDB_ORG", "smart-helmet")
        self.bucket = bucket or os.getenv("INFLUXDB_BUCKET", "helmet")

        if not self.token:
            raise ValueError(
                "INFLUXDB_TOKEN is not set. "
                "Set it as an environment variable before running."
            )

        self.client = InfluxDBClient(
            url=self.url,
            token=self.token,
            org=self.org,
        )

        self.write_api = self.client.write_api(
            write_options=SYNCHRONOUS
        )

    def write_point(self, point: Point) -> None:
        """Write one Point to InfluxDB."""

        self.write_api.write(
            bucket=self.bucket,
            org=self.org,
            record=point,
        )

    def close(self) -> None:
        """Close the InfluxDB client."""

        self.client.close()
