#!/usr/bin/env python3
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connection import db
from schedulers.token_cleanup import TokenCleanupScheduler
from schedulers.token_count_reset import TokenCountResetScheduler

async def test_token_cleanup():
    print("\n" + "="*50)
    print("Testing Token Cleanup Scheduler")
    print("="*50 + "\n")
    
    await db.connect()
    
    scheduler = TokenCleanupScheduler()
    await scheduler.cleanup_expired_tokens()
    
    await db.close()
    
    print("\n✅ Token cleanup test completed\n")

async def test_token_count_reset():
    print("\n" + "="*50)
    print("Testing Token Count Reset Scheduler")
    print("="*50 + "\n")
    
    await db.connect()
    
    scheduler = TokenCountResetScheduler()
    await scheduler.reset_token_counts()
    
    await db.close()
    
    print("\n✅ Token count reset test completed\n")

async def main():
    print("\n🧪 Scheduler Test Runner\n")
    print("Select a test:")
    print("1. Token Cleanup")
    print("2. Token Count Reset")
    print("3. Run All Tests")
    print("0. Exit\n")
    
    choice = input("Enter choice: ").strip()
    
    if choice == "1":
        await test_token_cleanup()
    elif choice == "2":
        await test_token_count_reset()
    elif choice == "3":
        await test_token_cleanup()
        await test_token_count_reset()
    elif choice == "0":
        print("Exiting...")
        return
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
