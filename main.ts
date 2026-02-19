import puppeteer from 'puppeteer-core';
import 'dotenv/config'

let instagram_session_id: string | undefined;

try {
    instagram_session_id = process.env["INSTAGRAM_SESSION_ID"]

    if (instagram_session_id === undefined) {
        throw Error()
    }
} catch {
    console.error("cannot load env")
    process.exit(1)
}

const browser = await puppeteer.launch({
    executablePath: "/usr/bin/chromium",
});

try {
    await browser.setCookie(
      {
        name: 'sessionid',
        value: instagram_session_id,
        domain: '.instagram.com',
        path: '/',
        expires: -1,
        httpOnly: true,
        secure: true,
    });
    const page = await browser.newPage();
    await page.setViewport({width: 1920, height: 1080});
    await page.goto("https://www.instagram.com/direct/inbox/");

    await page.waitForFunction(() => {
        const crappy_bar = document.body.children[6].children[0].children[0].children[1].children[0].children[0].children[0].children[0].children[0].children[0].children[0].children[0]
        
        if (crappy_bar === undefined) return;
        
        crappy_bar.remove();
        return true;
    })
    await page.waitForFunction(() => {
        const button = document.getElementsByTagName("button")[2]
        
        if (button === undefined || button.textContent.search(/Not Now/) < 0) {
            return;
        }
        
        button.click();
        return true;
    })
    const handle = await page.waitForFunction(() => document.getElementsByTagName("h1")[0].parentElement.parentElement.children[2])

    
    await handle.screenshot({
        path: "work/new.png",
        clip: {
            x: 87,
            y: 0,
            width: 13,
            height: 10000,
        },
        captureBeyondViewport: false
    });

    console.log("success")
} finally {
    await browser.close()
}