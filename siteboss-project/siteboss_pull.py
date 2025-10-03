#!/usr/bin/env python3
import asyncio
import argparse
from pathlib import Path
from playwright.async_api import async_playwright

async def fetch_xml(host: str, username: str, password: str, out_file: str) -> int:
    base = f'http://{host}'
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context()
        page = await ctx.new_page()

        # 1) Open login page
        await page.goto(f'{base}/UnitLogin.html', wait_until='domcontentloaded')
        # 2) AJAX login
        await page.evaluate(
            """
            async (cred)=>{
              const params = new URLSearchParams({username:cred.u, password:cred.p});
              await fetch('/index.html?commit=login', {
                method:'POST',
                headers:{'Content-Type':'application/x-www-form-urlencoded','X-Requested-With':'XMLHttpRequest'},
                body:params
              });
            }
            """,
            {"u": username, "p": password}
        )
        # 3) Land on UI to cement session
        await page.goto(f'{base}/UnitMain.html', wait_until='domcontentloaded')
        
        # 4) Navigate directly to XML and read response text
        resp = await page.goto(f'{base}/SiteStatus.xml')
        xml_text = await resp.text()

        Path(out_file).write_text(xml_text)
        print('Saved XML ->', out_file)

        await browser.close()
        return 0 if xml_text.strip().startswith('<?xml') else 1

async def main_async():
    ap = argparse.ArgumentParser(description='SiteBoss XML puller (Playwright)')
    ap.add_argument('--host', required=True)
    ap.add_argument('--user', required=True)
    ap.add_argument('--pass', dest='password', required=True)
    ap.add_argument('--out', default='SiteStatus.xml')
    args = ap.parse_args()
    rc = await fetch_xml(args.host, args.user, args.password, args.out)
    raise SystemExit(rc)

if __name__ == '__main__':
    asyncio.run(main_async())
