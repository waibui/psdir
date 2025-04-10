# -*- coding: utf-8 -*-
#  psdir - Web Path Scanner
#  Copyright (c) 2025 waibui
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from core.config import Config

def print_config(args, wordlist):
    """Prints the scanning configuration based on the provided arguments and wordlist.

    Args:
        args (argparse.Namespace): The object containing configuration parameters.
        wordlist (list): A list of keywords to be scanned.

    Output:
        Prints the scanning configuration details to the console.
    """
    print(Config.SEPARATOR)
    print(f"- Target URL: {args.url}")
    print(f"- Threads: {args.concurrency}")
    print(f"- Timeout: {args.timeout} seconds")
    print(f"- Allow Redirects: {'Yes' if args.allow_redirect else 'No'}")
    print(f"- Cookie: {args.cookie if args.cookie else 'None'}")
    print(f"- Proxy: {args.proxies if args.proxies else 'None'}")
    print(f"- Wordlist: {args.wordlist} ({len(wordlist)} entries)")
    print(f"- Target Status Codes: {args.match_code}")
    print(Config.SEPARATOR)
    
def print_results(total_time, results, status_count):
    """
    Prints a comprehensive summary of the scan results, including:
    - Total scan time.
    - HTTP status code summary.
    - Total URLs scanned.
    - Number of valid URLs found.
    
    Parameters:
    - total_time (float): The total time taken for the scan, in seconds.
    """
    # Print scan results summary
    if not results:
        print("No matching paths found.")

    print(Config.SEPARATOR)
    print(f"[+] Scan Completed in {total_time:.2f}s")
    for status, count in sorted(status_count.items()):
        print(f"- {status}: {count} occurrences")
    print(Config.SEPARATOR)