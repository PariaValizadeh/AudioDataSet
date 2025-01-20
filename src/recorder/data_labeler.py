import csv
import os
import logging

class DataLabeler:
    def __init__(self, labels_file):
        self.labels_file = labels_file
        self.logger = logging.getLogger(__name__)
        if not os.path.exists(labels_file):
            with open(labels_file, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["filename", "hardware", "channel", "DOA", "elevation", "category", "frequency", "gain", "amplitude", "length"])  # Header row

    def add_labels(self, metadata, data):
        with open(self.labels_file, mode="a", newline="") as f:
            writer = csv.writer(f)
            for datum in data:
                writer.writerow([datum['filename'], datum['hardware'], datum['channel'], datum['DOA'], datum['elevation'], datum['category'], datum['frequency'], datum['gain'], datum['amplitude'], datum['length']])  # Full metadata
                self.logger.info(f"Labeled data: {datum['filename']}")
