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
#
#  Author: waibui
#  Email: waibui@example.com
#  Website: https://github.com/waibui

import aiohttp
import time
from lxml import html
from urllib.parse import urljoin, urlparse
from utils.user_agent import random_user_agent
from utils.logger import Logger
from model.result import Result

async def request(session, path, user_agent, args):
    full_url = f"{args.url.rstrip('/')}/{path.lstrip('/')}"
    headers = {"User-Agent": random_user_agent(user_agent)}
    
    kwargs = {
        "headers": headers,
        "timeout": aiohttp.ClientTimeout(total=args.timeout),
        "allow_redirects": args.allow_redirect
    }

    if args.cookie:
        kwargs["cookies"] = args.cookie
    if args.proxies:
        kwargs["proxy"] = args.proxies

    start_time = time.time()
    try:    
        async with session.get(full_url, **kwargs) as response:
            elapsed_time = time.time() - start_time  

            result = None
            if response.status in args.match_code:
                Logger.info(f"[+] {response.status} - {elapsed_time:.3f}s - {full_url}")
                result = Result(response.status, full_url, elapsed_time)
                
                if args.scrape and response.status == 200:
                    content = await response.text()
                    links = extract_links(full_url, content, args)
                    return result, links
            return result, []
    except aiohttp.ClientError:
        pass
    except Exception as e:
        pass
    return None, []

def extract_links(base_url, html_content, args):
    crawled_links = set()
    extracted_links = []
    try:
        if not html_content.strip():
            return []

        if isinstance(html_content, str):
            html_content = html_content.encode('utf-8')

        tree = html.fromstring(html_content)
        links = []

        for link in tree.xpath('//a[@href]'):
            href = link.get('href')
            if href:
                absolute_url = urljoin(base_url, href)
                if (absolute_url not in crawled_links and 
                    not href.startswith('#') and 
                    not href.startswith('javascript:') and
                    not href.startswith('mailto:') and
                    not href.startswith('tel:')):

                    base_domain = urlparse(args.url).netloc
                    link_domain = urlparse(absolute_url).netloc

                    if base_domain == link_domain:
                        links.append(absolute_url)
                        crawled_links.add(absolute_url)
                        extracted_links.append(absolute_url)

        return links
    except Exception as e:
        return []

async def check_link_status(session, url, user_agent, args):
    headers = {"User-Agent": random_user_agent(user_agent)}
    kwargs = {
        "headers": headers,
        "timeout": aiohttp.ClientTimeout(total=args.timeout),
        "allow_redirects": args.allow_redirect
    }

    if args.cookie:
        kwargs["cookies"] = args.cookie
    if args.proxies:
        kwargs["proxy"] = args.proxies

    start_time = time.time()
    try:
        async with session.get(url, **kwargs) as response:
            elapsed_time = time.time() - start_time
            if response.status in args.match_code:
                Logger.info(f"[+] {response.status} - {elapsed_time:.3f}s - {url} (extracted link)")

                result = Result(response.status, url, elapsed_time)
                return result
    except aiohttp.ClientError as e:
        pass
    except Exception as e:
        pass

    return None