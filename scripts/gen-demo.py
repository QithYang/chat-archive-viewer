#!/usr/bin/env python3
"""Generate the sample data: demo-conversations.json (English) and
demo-conversations.zh.json (Chinese).

Each file keeps its three hand-written conversations (demo-conv-001..003) as
they are and adds generated ones (demo-conv-g001...) spread over the six
months before them, so the statistics view has something to show. Everything
here is made up.

Every conversation is written out in full below (title, question, answer,
optional thinking, optional closing exchange), so nothing is stitched
together at random; the script only decides *when* each one happens. Both
languages use mirrored lists and one seed, so their timelines and charts
match. The output is deterministic; re-run after editing:

    python3 scripts/gen-demo.py

Times are planned in UTC+8 and stored as UTC with a Z suffix.
"""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTS = {"en": ROOT / "demo-conversations.json", "zh": ROOT / "demo-conversations.zh.json"}
CN = timezone(timedelta(hours=8))
START = datetime(2025, 11, 1, tzinfo=CN)
END = datetime(2026, 4, 3, tzinfo=CN)  # hand-written samples start 2026-04-05
SEED = 20261003

# One-question conversations: (title, question, answer, thinking or None).
# Index i in "zh" and "en" is the same conversation.
THREADS = {
    "zh": [
        ("Python 列表推导式", "列表推导式和 for 循环比，有什么好处？", "主要是简洁：`[x*2 for x in nums]` 一行就能表达「把每个元素翻倍」。性能上通常也略快一些，因为循环在解释器内部完成。不过逻辑复杂时，普通 for 循环更好读。", "用户在问基础概念，先给结论再举一个小例子。"),
        ("merge 还是 rebase", "git merge 和 rebase 该用哪个？", "简单原则：\n\n- **merge** 保留真实的分支历史，适合合并到公共分支\n- **rebase** 让历史变成一条直线，适合整理自己还没推送的提交\n\n别对已经推送、别人也在用的分支做 rebase。", "这里最容易混淆的是使用场景，按场景回答。"),
        ("IndexError 报错", "这个报错是什么意思：`IndexError: list index out of range`", "说明你访问的下标超出了列表长度。比如列表只有 3 个元素，下标最大是 2，却访问了 `items[3]`。可以先 `print(len(items))` 看看实际长度。", None),
        ("正则的贪婪匹配", "正则里 `.*?` 和 `.*` 有什么区别？", "`.*` 是贪婪匹配，会尽可能多地吃字符；`.*?` 是非贪婪，匹配到最短就停。比如在 `<a><b>` 里用 `<.*>` 会匹配整串，用 `<.*?>` 只匹配 `<a>`。", "用一个具体字符串对比两种结果，最直观。"),
        ("SQL 查询变慢", "SQL 查询很慢，先从哪里查？", "先用 `EXPLAIN` 看执行计划，重点看有没有全表扫描。常见的改进：给 WHERE 和 JOIN 用到的列加索引、避免在索引列上套函数、只取需要的列而不是 `SELECT *`。", None),
        ("flex 垂直居中", "flex 布局里怎么让元素垂直居中？", "父元素加上：\n\n```css\ndisplay: flex;\nalign-items: center;\n```\n\n如果水平也要居中，再加 `justify-content: center;`。", "给出可以直接复制的代码片段会更有用。"),
        ("一长串 if/elif", "我的代码里有一长串 if/elif，按类型返回不同的提示语，怎么简化？", "可以用字典把类型映射到提示语：`MESSAGES = {'a': '…', 'b': '…'}`，然后 `MESSAGES.get(kind, '默认提示')`。以后新增一种类型只要加一行。", None),
        ("写爬虫的注意事项", "写爬虫要注意什么？", "几件事：先看网站的 robots.txt 和使用条款；请求之间加间隔，别给对方服务器压力；做好异常处理和重试；数据只用于自己被允许的用途。", None),
        ("affect 和 effect", "affect 和 effect 怎么区分？", "多数情况下 **affect** 是动词（影响），**effect** 是名词（效果）。记法：*A for action*，动作用 affect。", "用户的语法点比较基础，用记忆口诀会更好记。"),
        ("改一个英文句子", "帮我把这句话改得更自然：I very like this book.", "可以说 *I really like this book.* 或 *I like this book a lot.* —— very 不能直接修饰动词。", "给一个改写示例，比讲规则更直观。"),
        ("雅思大作文开头", "雅思大作文开头怎么写比较稳？", "一个稳妥的结构：一句改写题目 + 一句表明立场。不用追求华丽，清楚比复杂更重要。", None),
        ("每天练口语", "我想练口语，每天该怎么安排？", "建议每天 20 分钟：5 分钟跟读、10 分钟就一个话题自言自语并录音、5 分钟回听找问题。坚持比时长更重要。", None),
        ("英文邮件结尾", "邮件结尾除了 Best regards 还能用什么？", "常见的有 *Kind regards*、*Many thanks*、*Cheers*（比较随意）。正式场合用 *Kind regards* 最保险。", None),
        ("look forward to 的用法", "look forward to 后面接什么？", "接名词或动名词：*I look forward to hearing from you.* 这里的 to 是介词，不是不定式。", None),
        ("by the way 正式吗", "by the way 在正式邮件里可以用吗？", "可以但偏口语。正式一点可以换成 *Additionally* 或 *Also*。", None),
        ("番茄炒蛋的顺序", "番茄炒蛋要先炒蛋还是先炒番茄？", "先炒蛋：油热下蛋液，凝固到七成就盛出。再炒番茄出汁，最后把蛋倒回去翻匀。这样蛋嫩、汁多。", None),
        ("鸡蛋土豆洋葱", "家里只有鸡蛋、土豆和洋葱，能做什么？", "可以做西班牙土豆蛋饼：土豆洋葱切薄片小火煎软，倒入蛋液，小火慢慢凝固，翻面再煎两分钟。", "用户手边食材有限，给一道能直接做的菜。"),
        ("烤箱预热", "烤箱要预热多久？", "一般 10–15 分钟，等到达设定温度的指示灯亮就行。烤蛋糕之类对温度敏感的，预热一定要充分。", None),
        ("米饭夹生", "米饭总是夹生，怎么办？", "多数是水少了或者没泡。大米和水大约 1:1.2，先泡 20 分钟再煮，煮好焖 10 分钟别急着开盖。", None),
        ("15 分钟晚饭", "有没有 15 分钟能做完的晚饭？", "试试葱油拌面：面煮好，热油浇在葱花、生抽、少许糖上，拌匀即可。再加个煎蛋就很完整。", None),
        ("炒青菜变黄", "怎么让炒青菜保持翠绿？", "大火快炒，下锅前确保锅够热；盐最后放；也可以先焯水 10 秒再炒。", None),
        ("京都三日行程", "京都三天怎么安排比较不赶？", "可以按区域分：第一天东山（清水寺、二年坂），第二天岚山，第三天伏见稻荷 + 市区。早上尽量早出门，避开人流。", "行程问题按区域拆分最清楚。"),
        ("冰岛自驾", "冰岛自驾要注意什么？", "注意天气和路况，出发前查 road.is；F 路需要四驱；加油站之间距离可能很远，半箱油就加。", None),
        ("行李清单", "短途旅行带什么最容易忘？", "充电器、常用药、证件复印件、一个折叠购物袋。可以列一个固定清单，每次照着核对。", None),
        ("旅行拍照", "旅行时怎么拍出好看的照片？", "多利用早晨和傍晚的光线；人物不一定放正中，试试三分构图；多拍几张再挑。", None),
        ("旅行保险", "出国玩要不要买旅行保险？", "建议买，尤其是医疗和行程延误保障。注意看清条款里对高风险活动的限制。", None),
        ("《百年孤独》人名", "《百年孤独》人名太多记不住怎么办？", "可以边读边画一张家族树，或者找一张现成的放在手边。读到一半之后你会发现名字的重复本身就是书的主题之一。", None),
        ("没时间读书", "每天没时间读书，怎么坚持？", "把目标定小：每天 10 页，或者睡前 15 分钟。随身带一本，零碎时间也能读几页。", "用户需要的是可执行的方法，不是泛泛的建议。"),
        ("科普书推荐", "推荐几本入门科普书？", "可以试试《时间简史》《自私的基因》《人类简史》。题材不同，挑你最感兴趣的那本先读。", None),
        ("读书笔记", "读书笔记怎么做才有用？", "别只抄原文。读完一章，用自己的话写三句：讲了什么、我同意什么、我能用在哪里。", None),
        ("纸质书还是电子书", "纸质书和电子书哪个更好？", "各有优点：纸质书更容易专注和回翻，电子书方便携带和搜索。看你主要在什么场景读。", None),
        ("零基础跑步", "零基础想开始跑步，怎么开始？", "从跑走结合开始：跑 1 分钟、走 2 分钟，重复 8 组。每周 3 次，逐渐增加跑的时间。", None),
        ("在家无器械训练", "在家没有器械能练什么？", "深蹲、俯卧撑、平板支撑、弓步蹲。每个动作 3 组，组间休息 1 分钟。", None),
        ("跑后膝盖疼", "跑完步膝盖有点疼，正常吗？", "轻微酸胀可能是不适应，但如果是刺痛或持续疼痛，建议先停跑并咨询医生。也检查一下跑鞋和步幅。", "涉及身体不适，提醒必要时就医。"),
        ("运动后拉伸", "运动后要拉伸多久？", "每个部位 20–30 秒，重点拉大腿前后侧、小腿和臀部，总共 5–10 分钟就够。", None),
        ("睡不着", "晚上总是睡不着怎么办？", "尽量固定起床时间，睡前一小时少看屏幕，下午之后少喝咖啡。如果长期失眠，最好咨询医生。", None),
        ("会议纪要模板", "帮我设计一个会议纪要模板", "可以包含：\n\n1. 时间、参会人\n2. 议题\n3. 结论\n4. 待办（负责人 + 截止时间）\n\n待办那一栏最重要。", "给一个能直接套用的结构。"),
        ("周报写成流水账", "周报总写成流水账，怎么改？", "按「结果—问题—下周计划」三段写，每段只列最重要的两三条。能用数字说明的尽量用数字。", None),
        ("先做哪件事", "事情太多，先做哪个？", "可以用紧急/重要四象限粗分一下，先做重要且紧急的；重要不紧急的要提前排进日程，不然它们会变成紧急的。", None),
        ("一页 PPT 的字数", "一页 PPT 放多少字合适？", "一页一个观点，标题就写结论。正文尽量不超过三行，细节放到讲稿里。", None),
        ("绿萝叶子发黄", "绿萝叶子发黄是怎么回事？", "常见原因是浇水太多或光线太少。等土表面干了再浇，放到明亮的散射光处。", None),
        ("给朋友的生日礼物", "朋友喜欢画画，送什么生日礼物好？", "可以考虑一套好一点的水彩、速写本，或者一节体验课。附一张手写卡片会更走心。", None),
        ("学吉他", "学吉他先练什么？", "先练几个基本和弦：C、G、Am、F（F 比较难，可以先用简化版）。每天 15 分钟，指尖会慢慢长茧。", None),
        ("猫为什么踩奶", "猫为什么会踩奶？", "这是小时候吃奶时留下的习惯，通常表示放松和满足。", None),
        ("下雨天做什么", "下雨天适合做什么？", "看一部电影、整理房间、做一锅汤，或者就听着雨声读本书。", None),
    ],
    "en": [
        ("Python list comprehensions", "What's the advantage of a list comprehension over a for loop?", "Mostly brevity: `[x*2 for x in nums]` says \"double every element\" in one line. It's usually a little faster too, since the loop runs inside the interpreter. When the logic gets complex, a plain for loop reads better.", "This is a basic concept; lead with the answer, then one small example."),
        ("Merge or rebase", "Should I use git merge or rebase?", "A simple rule:\n\n- **merge** keeps the real branch history; use it when merging into shared branches\n- **rebase** makes the history a straight line; use it to tidy commits you haven't pushed yet\n\nDon't rebase a branch that's already pushed and used by others.", "The usual confusion is when to use which, so answer by situation."),
        ("An IndexError", "What does this error mean: `IndexError: list index out of range`", "You accessed an index past the end of the list. If the list has 3 items, the highest index is 2, but the code asked for `items[3]`. Try `print(len(items))` to see the real length.", None),
        ("Greedy regex matching", "What's the difference between `.*?` and `.*` in a regex?", "`.*` is greedy and takes as many characters as it can; `.*?` is lazy and stops at the shortest match. On `<a><b>`, `<.*>` matches the whole string while `<.*?>` matches just `<a>`.", "Comparing both on one concrete string shows it best."),
        ("A slow SQL query", "My SQL query is slow. Where do I start?", "Run `EXPLAIN` and look for full table scans. Common fixes: index the columns used in WHERE and JOIN, avoid wrapping indexed columns in functions, and select only the columns you need instead of `SELECT *`.", None),
        ("Vertical centering with flexbox", "How do I vertically center an element with flexbox?", "On the parent:\n\n```css\ndisplay: flex;\nalign-items: center;\n```\n\nAdd `justify-content: center;` to center it horizontally as well.", "A snippet they can copy will help most."),
        ("A long if/elif chain", "My code has a long if/elif chain that returns a different message for each type. How can I simplify it?", "Map types to messages with a dictionary: `MESSAGES = {'a': '…', 'b': '…'}`, then `MESSAGES.get(kind, 'default message')`. Adding a new type then takes one line.", None),
        ("Writing a scraper", "What should I watch out for when writing a scraper?", "A few things: read the site's robots.txt and terms first; space out your requests so you don't load their server; handle errors and retries; and only use the data in ways you're allowed to.", None),
        ("Affect or effect", "How do I tell affect and effect apart?", "Most of the time **affect** is the verb and **effect** is the noun. A memory aid: *A for action*, so the action word is affect.", "A memory aid will stick better than a grammar rule here."),
        ("Fixing one sentence", "Can you make this sentence sound more natural: I very like this book.", "Try *I really like this book.* or *I like this book a lot.* — very can't modify a verb directly.", "One rewritten example says more than an explanation."),
        ("Opening an essay", "What's a safe way to open an argumentative essay?", "One reliable shape: one sentence restating the question, one sentence stating your position. Clear beats fancy.", None),
        ("Daily speaking practice", "I want to get better at speaking. How should I plan each day?", "About 20 minutes: 5 minutes shadowing a recording, 10 minutes talking to yourself about one topic while recording, 5 minutes listening back for mistakes. Consistency matters more than length.", None),
        ("Ending an email", "What can I use instead of Best regards to end an email?", "Common ones are *Kind regards*, *Many thanks* and *Cheers* (more casual). *Kind regards* is the safest in formal settings.", None),
        ("Look forward to", "What comes after look forward to?", "A noun or an -ing form: *I look forward to hearing from you.* The to here is a preposition, not part of an infinitive.", None),
        ("Is by the way formal?", "Is by the way fine in a formal email?", "It works but sounds conversational. *Additionally* or *Also* reads a bit more formal.", None),
        ("Tomato and egg stir-fry", "For tomato and egg stir-fry, do the eggs or the tomatoes go first?", "Eggs first: pour them into hot oil and take them out when they're about 70% set. Then cook the tomatoes until they release their juice and fold the eggs back in. The eggs stay tender and the sauce stays juicy.", None),
        ("Eggs, potatoes, onion", "I only have eggs, potatoes and an onion. What can I make?", "A Spanish tortilla: slice the potato and onion thinly and cook them gently until soft, pour in the beaten eggs, let it set over low heat, then flip and cook two more minutes.", "They have few ingredients, so suggest one dish they can make right now."),
        ("Preheating the oven", "How long should I preheat the oven?", "Usually 10–15 minutes, until the indicator says it has reached temperature. For cakes and other temperature-sensitive bakes, make sure it's fully preheated.", None),
        ("Undercooked rice", "My rice keeps coming out undercooked. What am I doing wrong?", "Usually too little water or no soaking. Use about 1:1.2 rice to water, soak for 20 minutes, and let it rest covered for 10 minutes after cooking.", None),
        ("A 15-minute dinner", "Any dinner I can make in 15 minutes?", "Scallion oil noodles: cook the noodles, pour hot oil over chopped scallions, soy sauce and a pinch of sugar, then toss. Add a fried egg and it's a full meal.", None),
        ("Keeping greens green", "How do I keep stir-fried greens bright green?", "High heat and a quick toss in a properly hot pan; salt at the end; or blanch them for 10 seconds first.", None),
        ("Three days in Kyoto", "How can I plan three days in Kyoto without rushing?", "Split it by area: day one Higashiyama (Kiyomizu-dera, Ninenzaka), day two Arashiyama, day three Fushimi Inari plus the city centre. Head out early to beat the crowds.", "An itinerary reads best split by area."),
        ("Driving in Iceland", "What should I know about driving in Iceland?", "Watch the weather and road conditions (check road.is before setting off); F-roads need four-wheel drive; petrol stations can be far apart, so fill up at half a tank.", None),
        ("Packing list", "What's easiest to forget on a short trip?", "Chargers, regular medication, copies of your documents and a folding shopping bag. Keep a fixed checklist and run through it each time.", None),
        ("Travel photos", "How do I take better travel photos?", "Use early morning and late afternoon light; don't always centre people, try the rule of thirds; take a few shots and pick the best.", None),
        ("Travel insurance", "Is travel insurance worth it for a trip abroad?", "Yes, especially medical cover and delay protection. Check the exclusions for higher-risk activities.", None),
        ("Names in One Hundred Years of Solitude", "There are too many names in One Hundred Years of Solitude. Any tips?", "Sketch a family tree as you go, or keep a printed one beside you. Halfway through you'll notice the repeating names are part of the point.", None),
        ("No time to read", "I never have time to read. How do I keep going?", "Make the goal small: 10 pages a day, or 15 minutes before bed. Carry a book with you so spare minutes count.", "They need a method they can act on, not general advice."),
        ("Popular science picks", "Can you recommend a few popular science books for beginners?", "Try *A Brief History of Time*, *The Selfish Gene* and *Sapiens*. They cover different ground, so start with the one that interests you most.", None),
        ("Reading notes", "How do I take reading notes that are actually useful?", "Don't just copy quotes. After each chapter, write three sentences in your own words: what it said, what you agree with, and where you could use it.", None),
        ("Paper or e-books", "Paper books or e-books?", "Each has its strengths: paper is easier to focus on and flip back through; e-books are easy to carry and search. It depends on where you usually read.", None),
        ("Starting to run", "I've never run before. How do I start?", "Start with run-walk intervals: run 1 minute, walk 2, repeat 8 times. Three times a week, and gradually lengthen the running parts.", None),
        ("Workouts without equipment", "What can I do at home without equipment?", "Squats, push-ups, planks and lunges. Three sets of each with a minute of rest between sets.", None),
        ("Knee pain after running", "My knee hurts a bit after running. Is that normal?", "Mild soreness can just be your body adjusting, but sharp or lasting pain means stop and see a doctor. Check your shoes and stride length too.", "This involves pain, so mention seeing a doctor when needed."),
        ("Stretching after a workout", "How long should I stretch after a workout?", "20–30 seconds per area, focusing on the front and back of the thighs, calves and glutes; 5–10 minutes in total is plenty.", None),
        ("Can't fall asleep", "I can't fall asleep at night. What helps?", "Keep a regular wake-up time, put screens away an hour before bed, and skip coffee after lunch. If it goes on for a long time, talk to a doctor.", None),
        ("Meeting notes template", "Can you design a meeting notes template for me?", "It could include:\n\n1. Date and attendees\n2. Topics\n3. Decisions\n4. Action items (owner + due date)\n\nThe action items matter most.", "Give a structure they can reuse as is."),
        ("Weekly updates", "My weekly updates read like a diary. How do I fix that?", "Use three parts: results, problems, next week's plan, with only the two or three most important points in each. Use numbers wherever you can.", None),
        ("What to do first", "I have too much to do. What comes first?", "Sort things roughly by urgent and important, and do the important-and-urgent ones first. Schedule the important-but-not-urgent ones ahead of time, or they'll turn urgent.", None),
        ("Text on a slide", "How much text should one slide have?", "One idea per slide, with the conclusion as the title. Keep the body to three lines or fewer and put details in your speaker notes.", None),
        ("Yellow pothos leaves", "Why are my pothos leaves turning yellow?", "Usually too much water or too little light. Water only once the topsoil is dry and move it somewhere with bright, indirect light.", None),
        ("A gift for a friend", "My friend loves painting. What's a good birthday gift?", "A good set of watercolours, a sketchbook, or a trial class. A handwritten card makes it more personal.", None),
        ("Learning guitar", "What should I practise first on guitar?", "A few basic chords: C, G, Am and F (F is hard, so start with the simplified version). Fifteen minutes a day and your fingertips will toughen up.", None),
        ("Why cats knead", "Why do cats knead?", "It's a habit from nursing as kittens and usually means the cat feels relaxed and content.", None),
        ("A rainy day", "What's good to do on a rainy day?", "Watch a film, tidy a room, cook a pot of soup, or just read with the rain in the background.", None),
    ],
}

# Closing exchanges, used as matched pairs: (user, assistant). Kept generic on
# purpose so they read naturally after any of the threads above.
CLOSINGS = {
    "zh": [("明白了，谢谢！", "不客气，有问题随时问。"), ("好的，谢谢！", "不客气～"),
           ("谢谢，很有帮助", "很高兴能帮上忙。")],
    "en": [("Got it, thanks!", "You're welcome, ask any time."), ("OK, thanks!", "Any time."),
           ("Thanks, that's really helpful", "Glad it helped.")],
}
THANKS_EMOJI = ["😊", "🙏", "✨", "👍"]

# Word of the day: (word, Chinese gloss, example sentence). 40 words, none repeated.
WORDS = [
    ("resilient", "有韧性的", "Kids are often more resilient than we think."),
    ("meticulous", "一丝不苟的", "She keeps meticulous notes for every project."),
    ("candid", "坦率的", "Thanks for your candid feedback on the draft."),
    ("ambiguous", "模棱两可的", "The instructions were ambiguous, so I asked again."),
    ("pragmatic", "务实的", "We took a pragmatic approach and fixed the biggest bug first."),
    ("vivid", "生动的", "He gave a vivid description of the old town."),
    ("coherent", "连贯的", "Her argument was clear and coherent."),
    ("diligent", "勤奋的", "A diligent student reviews her notes every evening."),
    ("eloquent", "雄辩的", "He gave an eloquent speech at the wedding."),
    ("frugal", "节俭的", "They live a frugal life and save most of their income."),
    ("genuine", "真诚的", "Her smile was warm and genuine."),
    ("humble", "谦逊的", "Despite his success, he stayed humble."),
    ("inevitable", "不可避免的", "Some mistakes are inevitable when you learn something new."),
    ("keen", "热衷的", "I'm keen to try the new café downstairs."),
    ("lucid", "清晰易懂的", "The book gives a lucid explanation of how vaccines work."),
    ("modest", "适度的", "We saw a modest improvement after the change."),
    ("notion", "概念，想法", "I had no notion of how long the trip would take."),
    ("obscure", "鲜为人知的", "He loves obscure bands that nobody has heard of."),
    ("plausible", "似乎合理的", "That sounds like a plausible explanation."),
    ("reluctant", "不情愿的", "She was reluctant to leave the party early."),
    ("subtle", "微妙的", "There's a subtle difference between the two shades of blue."),
    ("tedious", "乏味的", "Filling in the same form every week is tedious."),
    ("versatile", "多用途的", "A cast-iron pan is surprisingly versatile."),
    ("whim", "一时的念头", "We booked the trip on a whim."),
    ("zeal", "热情", "He started the new job with great zeal."),
    ("abundant", "丰富的", "Fresh fruit is abundant in summer."),
    ("brisk", "轻快的", "We took a brisk walk before breakfast."),
    ("cherish", "珍惜", "I cherish the letters my grandmother wrote."),
    ("dwell", "老是想着", "Try not to dwell on small mistakes."),
    ("endeavor", "努力", "Learning a language is a long endeavor."),
    ("fragile", "易碎的", "Please be careful, the vase is fragile."),
    ("grasp", "理解，领会", "It took me a while to grasp the idea."),
    ("hinder", "妨碍", "Noise can hinder your concentration."),
    ("imply", "暗示", "His silence seemed to imply agreement."),
    ("juggle", "同时应付", "She juggles work and evening classes."),
    ("linger", "逗留", "The smell of coffee lingered in the kitchen."),
    ("mundane", "平凡的", "Even mundane tasks feel better with music on."),
    ("novice", "新手", "As a novice cook, I follow recipes exactly."),
    ("optimistic", "乐观的", "I'm optimistic about the results."),
    ("persevere", "坚持不懈", "If you persevere, the chords will get easier."),
]


def word_turn(lang, w):
    word, gloss, example = w
    if lang == "zh":
        return (f"今天的单词：{word}", f"**{word}** —— {gloss}。\n\n> {example}")
    return (f"Word of the day: {word}", f"**{word}** — for example:\n\n> {example}")


def run_turns(lang, days):
    """(user, assistant) for each logged day of a beginner's plan: the distance
    only grows, every fourth day is a rest day, and the first 5 km happens once."""
    km, hit5 = 2.0, False
    for i in range(days):
        if i % 4 == 3:
            yield (("打卡：休息日，拉伸 10 分钟", "休息也是训练的一部分，明天继续。") if lang == "zh"
                   else ("Check-in: rest day, 10 minutes of stretching", "Rest is part of training too. Back at it tomorrow."))
            continue
        km = min(5.0, round(km + 0.25, 2))
        if km >= 5.0 and not hit5:
            hit5 = True
            yield (("打卡：5 公里！第一次一口气跑完 🎉", "太棒了！从 2 公里到 5 公里，坚持下来了。记得好好拉伸。") if lang == "zh"
                   else ("Check-in: 5 km! First time without stopping 🎉", "Brilliant! From 2 km to 5 km, and you stuck with it. Stretch well tonight."))
            continue
        secs = round((7.6 - i * 0.03) * 60)
        pace = f"{secs // 60}:{secs % 60:02d}"
        if lang == "zh":
            yield (f"打卡：{km:g} 公里，配速 {pace}", "很稳，比上周又快了一点。" if i >= 7 and i % 3 == 0 else "不错，保持这个节奏。")
        else:
            yield (f"Check-in: {km:g} km at {pace}/km", "Steady, and a bit faster than last week." if i >= 7 and i % 3 == 0 else "Nice, keep that rhythm.")


def cn_time(day, hour, minute):
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=CN)


def z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Conv:
    def __init__(self, n, title):
        self.n, self.title, self.msgs = n, title, []

    def add(self, sender, t, text, think=None, think_secs=0):
        content = []
        if think:
            content.append({"type": "thinking", "thinking": think,
                            "start_timestamp": z(t - timedelta(seconds=think_secs)), "stop_timestamp": z(t)})
        content.append({"type": "text", "text": text})
        self.msgs.append({"uuid": f"demo-g{self.n:03d}-m{len(self.msgs) + 1}",
                          "sender": sender, "created_at": z(t), "content": content})

    def to_json(self):
        return {"uuid": f"demo-conv-g{self.n:03d}", "name": self.title, "summary": "",
                "created_at": self.msgs[0]["created_at"], "updated_at": self.msgs[-1]["created_at"],
                "chat_messages": self.msgs}


def build(lang):
    rng = random.Random(SEED)

    def pick_hour(deep=False):
        if deep:
            return rng.choice([2, 2, 3, 3, 4])
        return rng.choices([8, 9, 10, 12, 13, 15, 17, 19, 20, 21, 22, 23],
                           [2, 3, 3, 4, 3, 2, 2, 4, 6, 7, 6, 3])[0]

    def pick_day():
        span = (END - START).days
        while True:
            d = START + timedelta(days=rng.randrange(span))
            if d.weekday() >= 5 or rng.random() < 0.3:  # weekends are busier
                return d

    convs = []
    for i, (title, q, a, think) in enumerate(THREADS[lang]):
        c = Conv(len(convs) + 1, title)
        t = cn_time(pick_day(), pick_hour(deep=(i % 9 == 4)), rng.randrange(60))
        c.add("human", t, q)
        t += timedelta(seconds=rng.randint(20, 90))
        c.add("assistant", t, a, think, rng.randint(3, 25))
        if rng.random() < 0.5:
            u, r = CLOSINGS[lang][rng.randrange(len(CLOSINGS[lang]))]
            if rng.random() < 0.4:
                u += " " + rng.choice(THANKS_EMOJI)
            t += timedelta(minutes=rng.randint(1, 6))
            c.add("human", t, u)
            c.add("assistant", t + timedelta(seconds=rng.randint(5, 20)), r)
        convs.append(c)

    def log(title, first_day, turns):
        c = Conv(len(convs) + 1, title)
        day = first_day
        for u, r in turns:
            if day >= END:
                break
            t = cn_time(day, pick_hour(), rng.randrange(60))
            c.add("human", t, u)
            c.add("assistant", t + timedelta(seconds=rng.randint(15, 60)), r)
            day += timedelta(days=rng.choice([1, 1, 1, 2]))
        convs.append(c)

    titles = {"zh": ["每日一词", "跑步记录", "每日一词 · 第二轮"],
              "en": ["Word of the day", "Running log", "Word of the day · round two"]}[lang]
    log(titles[0], datetime(2025, 11, 3, tzinfo=CN), [word_turn(lang, w) for w in WORDS[:24]])
    log(titles[1], datetime(2026, 1, 5, tzinfo=CN), list(run_turns(lang, 34)))
    log(titles[2], datetime(2026, 2, 16, tzinfo=CN), [word_turn(lang, w) for w in WORDS[24:]])

    out_path = OUTS[lang]
    existing = json.loads(out_path.read_text(encoding="utf-8"))
    hand = [c for c in existing if not c["uuid"].startswith("demo-conv-g")]
    out = hand + [c.to_json() for c in convs]
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    msgs = sum(len(c["chat_messages"]) for c in out)
    print(f"{out_path.name}: {len(out)} conversations, {msgs} messages, {out_path.stat().st_size // 1024} KB")


def main():
    assert len(THREADS["zh"]) == len(THREADS["en"])
    for zh, en in zip(THREADS["zh"], THREADS["en"]):
        assert (zh[3] is None) == (en[3] is None), zh[0]
    for lang in OUTS:
        build(lang)


if __name__ == "__main__":
    main()
