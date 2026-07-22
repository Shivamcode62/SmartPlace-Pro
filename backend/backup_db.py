#!/usr/bin/env python3
"""
Database backup script for SmartPlace Pro
"""

import os
import shutil
from datetime import datetime

def backup_database():
    """Backup the database"""
    db_path = "data/smartplace.db"
    backup_dir = "backups"
    
    if not os.path.exists(db_path):
        print("❌ Database not found")
        return
    
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"{backup_dir}/smartplace_backup_{timestamp}.db"
    
    shutil.copy2(db_path, backup_file)
    print(f"✅ Database backed up to {backup_file}")

if __name__ == "__main__":
    backup_database()