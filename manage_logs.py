

import os
import logging 
import argparse

def manage_logs(args=)

if __name__ == "__main__":
    
    """
    -h: help
    
    -ar: Archive
    -pg: Purge
    """
    parser = argparse.ArgumentParser(description="Script to archive or purge log files.")
    parser.add_argument("-ar", "--archive", action="store_true", help="Archive log files")
    parser.add_argument("-pg", "--purge", action="store_true", help="Purge log files")
    
    args = parser.parse_args()
    
    pass