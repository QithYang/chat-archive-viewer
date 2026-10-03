#!/usr/bin/env python3
"""Generate the sample data in demo-conversations.json.

Keeps the three hand-written conversations (demo-conv-001..003) as they are
and adds ~50 generated ones (demo-conv-g001...) spread over the six months
before them, so the statistics view has something to show. Everything here
is made up. The output is deterministic (fixed seed); re-run after editing:

    python3 scripts/gen-demo.py

Times are planned in UTC+8 and stored as UTC with a Z suffix.
"""
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo-conversations.json"
CN = timezone(timedelta(hours=8))
START = datetime(2025, 10, 6, tzinfo=CN)
END = datetime(2026, 4, 3, tzinfo=CN)  # hand-written samples start 2026-04-05

rng = random.Random(20261003)

EMOJI = ["😊", "👍", "🙏", "✨", "😂", "🤔", "❤️", "🎉", "😮", "🌙", "☕", "👨‍💻", "🧑‍🍳"]

# Each topic: titles, (question, answer) pairs, and optional short thinking notes.
TOPICS = {
    "code": {
        "titles": ["Python 列表推导式", "Git 分支怎么合并", "写一个小爬虫", "正则表达式入门", "SQL 查询优化", "前端布局问题"],
        "pairs": [
            ("列表推导式和 for 循环比，有什么好处？", "主要是简洁：`[x*2 for x in nums]` 一行就能表达「把每个元素翻倍」。性能上通常也略快一些，因为循环在解释器内部完成。不过逻辑复杂时，普通 for 循环更好读。"),
            ("git merge 和 rebase 该用哪个？", "简单原则：\n\n- **merge** 保留真实的分支历史，适合合并到公共分支\n- **rebase** 让历史变成一条直线，适合整理自己还没推送的提交\n\n别对已经推送、别人也在用的分支做 rebase。"),
            ("这个报错是什么意思：`IndexError: list index out of range`", "说明你访问的下标超出了列表长度。比如列表只有 3 个元素，下标最大是 2，却访问了 `items[3]`。可以先 `print(len(items))` 看看实际长度。"),
            ("正则里 `.*?` 和 `.*` 有什么区别？", "`.*` 是贪婪匹配，会尽可能多地吃字符；`.*?` 是非贪婪，匹配到最短就停。比如在 `<a><b>` 里用 `<.*>` 会匹配整串，用 `<.*?>` 只匹配 `<a>`。"),
            ("SQL 查询很慢，先从哪里查？", "先用 `EXPLAIN` 看执行计划，重点看有没有全表扫描。常见的改进：给 WHERE 和 JOIN 用到的列加索引、避免在索引列上套函数、只取需要的列而不是 `SELECT *`。"),
            ("flex 布局里怎么让元素垂直居中？", "父元素加上：\n\n```css\ndisplay: flex;\nalign-items: center;\n```\n\n如果水平也要居中，再加 `justify-content: center;`。"),
            ("能帮我看看这段代码哪里可以简化吗？", "可以把重复的判断提成一个小函数，再用字典代替一长串 if/elif。这样新增情况时只需要加一行映射。"),
            ("写爬虫要注意什么？", "几件事：先看网站的 robots.txt 和使用条款；请求之间加间隔，别给对方服务器压力；做好异常处理和重试；数据只用于自己被允许的用途。"),
        ],
        "think": ["用户在问基础概念，先给结论再举一个小例子。", "这里最容易混淆的是使用场景，按场景回答。", "给出可以直接复制的代码片段会更有用。"],
    },
    "english": {
        "titles": ["英语口语练习", "雅思写作思路", "这个单词怎么用", "英文邮件润色"],
        "pairs": [
            ("affect 和 effect 怎么区分？", "多数情况下 **affect** 是动词（影响），**effect** 是名词（效果）。记法：*A for action*，动作用 affect。"),
            ("帮我把这句话改得更自然：I very like this book.", "可以说 *I really like this book.* 或 *I like this book a lot.* —— very 不能直接修饰动词。"),
            ("雅思大作文开头怎么写比较稳？", "一个稳妥的结构：一句改写题目 + 一句表明立场。不用追求华丽，清楚比复杂更重要。"),
            ("我想练口语，每天该怎么安排？", "建议每天 20 分钟：5 分钟跟读、10 分钟就一个话题自言自语并录音、5 分钟回听找问题。坚持比时长更重要。"),
            ("邮件结尾除了 Best regards 还能用什么？", "常见的有 *Kind regards*、*Many thanks*、*Cheers*（比较随意）。正式场合用 *Kind regards* 最保险。"),
            ("look forward to 后面接什么？", "接名词或动名词：*I look forward to hearing from you.* 这里的 to 是介词，不是不定式。"),
            ("by the way 在正式邮件里可以用吗？", "可以但偏口语。正式一点可以换成 *Additionally* 或 *Also*。"),
        ],
        "think": ["用户的语法点比较基础，用记忆口诀会更好记。", "给一个改写示例，比讲规则更直观。"],
    },
    "cook": {
        "titles": ["番茄炒蛋怎么更好吃", "周末做什么菜", "烤箱新手问题", "一人食快手菜"],
        "pairs": [
            ("番茄炒蛋要先炒蛋还是先炒番茄？", "先炒蛋：油热下蛋液，凝固到七成就盛出。再炒番茄出汁，最后把蛋倒回去翻匀。这样蛋嫩、汁多。"),
            ("家里只有鸡蛋、土豆和洋葱，能做什么？", "可以做西班牙土豆蛋饼：土豆洋葱切薄片小火煎软，倒入蛋液，小火慢慢凝固，翻面再煎两分钟。"),
            ("烤箱要预热多久？", "一般 10–15 分钟，等到达设定温度的指示灯亮就行。烤蛋糕之类对温度敏感的，预热一定要充分。"),
            ("米饭总是夹生，怎么办？", "多数是水少了或者没泡。大米和水大约 1:1.2，先泡 20 分钟再煮，煮好焖 10 分钟别急着开盖。"),
            ("有没有 15 分钟能做完的晚饭？", "试试葱油拌面：面煮好，热油浇在葱花、生抽、少许糖上，拌匀即可。再加个煎蛋就很完整。"),
            ("怎么让炒青菜保持翠绿？", "大火快炒，下锅前确保锅够热；盐最后放；也可以先焯水 10 秒再炒。"),
        ],
        "think": ["用户手边食材有限，给一道能直接做的菜。"],
    },
    "travel": {
        "titles": ["京都三日行程", "第一次去冰岛", "周末短途去哪", "行李清单"],
        "pairs": [
            ("京都三天怎么安排比较不赶？", "可以按区域分：第一天东山（清水寺、二年坂），第二天岚山，第三天伏见稻荷 + 市区。早上尽量早出门，避开人流。"),
            ("冰岛自驾要注意什么？", "注意天气和路况，出发前查 road.is；F 路需要四驱；加油站之间距离可能很远，半箱油就加。"),
            ("短途旅行带什么最容易忘？", "充电器、常用药、证件复印件、一个折叠购物袋。可以列一个固定清单，每次照着核对。"),
            ("旅行时怎么拍出好看的照片？", "多利用早晨和傍晚的光线；人物不一定放正中，试试三分构图；多拍几张再挑。"),
            ("要不要买旅行保险？", "出境的话建议买，尤其是医疗和行程延误保障。注意看清条款里对高风险活动的限制。"),
        ],
        "think": ["行程问题按区域拆分最清楚。"],
    },
    "reading": {
        "titles": ["《百年孤独》读后感", "怎么坚持读书", "推荐几本科普书", "读书笔记方法"],
        "pairs": [
            ("《百年孤独》人名太多记不住怎么办？", "可以边读边画一张家族树，或者找一张现成的放在手边。读到一半之后你会发现名字的重复本身就是书的主题之一。"),
            ("每天没时间读书，怎么坚持？", "把目标定小：每天 10 页，或者睡前 15 分钟。随身带一本，零碎时间也能读几页。"),
            ("推荐几本入门科普书？", "可以试试《时间简史》《自私的基因》《人类简史》。题材不同，挑你最感兴趣的那本先读。"),
            ("读书笔记怎么做才有用？", "别只抄原文。读完一章，用自己的话写三句：讲了什么、我同意什么、我能用在哪里。"),
            ("纸质书和电子书哪个更好？", "各有优点：纸质书更容易专注和回翻，电子书方便携带和搜索。看你主要在什么场景读。"),
        ],
        "think": ["用户需要的是可执行的方法，不是泛泛的建议。"],
    },
    "fitness": {
        "titles": ["新手跑步计划", "在家练什么", "拉伸动作", "怎么改善睡眠"],
        "pairs": [
            ("零基础想开始跑步，怎么开始？", "从跑走结合开始：跑 1 分钟、走 2 分钟，重复 8 组。每周 3 次，逐渐增加跑的时间。"),
            ("在家没有器械能练什么？", "深蹲、俯卧撑、平板支撑、弓步蹲。每个动作 3 组，组间休息 1 分钟。"),
            ("跑完步膝盖有点疼，正常吗？", "轻微酸胀可能是不适应，但如果是刺痛或持续疼痛，建议先停跑并咨询医生。也检查一下跑鞋和步幅。"),
            ("运动后要拉伸多久？", "每个部位 20–30 秒，重点拉大腿前后侧、小腿和臀部，总共 5–10 分钟就够。"),
            ("晚上总是睡不着怎么办？", "尽量固定起床时间，睡前一小时少看屏幕，下午之后少喝咖啡。如果长期失眠，最好咨询医生。"),
        ],
        "think": ["涉及身体不适，提醒必要时就医。"],
    },
    "work": {
        "titles": ["会议纪要模板", "周报怎么写", "时间管理", "做一页 PPT"],
        "pairs": [
            ("帮我设计一个会议纪要模板", "可以包含：\n\n1. 时间、参会人\n2. 议题\n3. 结论\n4. 待办（负责人 + 截止时间）\n\n待办那一栏最重要。"),
            ("周报总写成流水账，怎么改？", "按「结果—问题—下周计划」三段写，每段只列最重要的两三条。能用数字说明的尽量用数字。"),
            ("事情太多，先做哪个？", "可以用紧急/重要四象限粗分一下，先做重要且紧急的；重要不紧急的要提前排进日程，不然它们会变成紧急的。"),
            ("一页 PPT 放多少字合适？", "一页一个观点，标题就写结论。正文尽量不超过三行，细节放到讲稿里。"),
        ],
        "think": ["给一个能直接套用的结构。"],
    },
    "misc": {
        "titles": ["养绿萝的问题", "给朋友挑生日礼物", "学吉他从哪开始", "猫为什么踩奶"],
        "pairs": [
            ("绿萝叶子发黄是怎么回事？", "常见原因是浇水太多或光线太少。等土表面干了再浇，放到明亮的散射光处。"),
            ("朋友喜欢画画，送什么生日礼物好？", "可以考虑一套好一点的水彩、速写本，或者一节体验课。附一张手写卡片会更走心。"),
            ("学吉他先练什么？", "先练几个基本和弦：C、G、Am、F（F 比较难，可以先用简化版）。每天 15 分钟，指尖会慢慢长茧。"),
            ("猫为什么会踩奶？", "这是小时候吃奶时留下的习惯，通常表示放松和满足。"),
            ("下雨天适合做什么？", "看一部电影、整理房间、做一锅汤，或者就听着雨声读本书。"),
        ],
        "think": [],
    },
}

FOLLOWUPS = ["好的，我试试", "明白了，谢谢！", "原来如此", "那如果换一种情况呢？", "有道理", "收到～"]
ACKS = ["不客气，有问题随时问。", "加油！", "试过之后可以告诉我效果。", "好的，有需要再来找我。"]

# Long check-in conversations: one short exchange per day, so repetition reads naturally.
WORDS = ["resilient", "meticulous", "candid", "ambiguous", "pragmatic", "vivid", "coherent", "diligent",
         "eloquent", "frugal", "genuine", "humble", "inevitable", "keen", "lucid", "modest", "notion",
         "obscure", "plausible", "reluctant", "subtle", "tedious", "versatile", "whim", "zeal",
         "abundant", "brisk", "cherish", "dwell", "endeavor", "fragile", "grasp", "hinder", "imply"]
RUNS = ["3 公里，配速 7:10", "跑走结合 25 分钟", "4 公里，比上次轻松", "休息日，拉伸 10 分钟",
        "3.5 公里，最后一公里加速", "5 公里！第一次跑完", "雨天在家做了 20 分钟力量"]


def cn_time(day, hour, minute):
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=CN)


def z(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pick_hour(deep=False):
    if deep:
        return rng.choice([2, 2, 3, 3, 4])
    return rng.choices([8, 9, 10, 12, 13, 15, 17, 19, 20, 21, 22, 23],
                       [2, 3, 3, 4, 3, 2, 2, 4, 6, 7, 6, 3])[0]


def pick_day():
    span = (END - START).days
    while True:
        d = START + timedelta(days=rng.randrange(span))
        # weekends are busier
        if d.weekday() >= 5 or rng.random() < 0.55:
            return d


def sprinkle(text):
    if rng.random() < 0.3:
        return text + " " + rng.choice(EMOJI)
    return text


class Conv:
    def __init__(self, n, title):
        self.n = n
        self.title = title
        self.msgs = []

    def add(self, sender, t, text, think=None):
        content = []
        if think:
            start = t - timedelta(seconds=rng.randint(3, 25))
            content.append({"type": "thinking", "thinking": think,
                            "start_timestamp": z(start), "stop_timestamp": z(t)})
        content.append({"type": "text", "text": text})
        self.msgs.append({"uuid": f"demo-g{self.n:03d}-m{len(self.msgs) + 1}",
                          "sender": sender, "created_at": z(t), "content": content})

    def to_json(self):
        return {"uuid": f"demo-conv-g{self.n:03d}", "name": self.title, "summary": "",
                "created_at": self.msgs[0]["created_at"], "updated_at": self.msgs[-1]["created_at"],
                "chat_messages": self.msgs}


def topic_conv(n, key, deep=False):
    topic = TOPICS[key]
    c = Conv(n, rng.choice(topic["titles"]))
    day = pick_day()
    t = cn_time(day, pick_hour(deep), rng.randrange(60))
    pairs = rng.sample(topic["pairs"], k=min(len(topic["pairs"]), rng.randint(1, 4)))
    for i, (q, a) in enumerate(pairs):
        c.add("human", t, sprinkle(q))
        t += timedelta(seconds=rng.randint(20, 90))
        think = rng.choice(topic["think"]) if topic["think"] and rng.random() < 0.4 else None
        c.add("assistant", t, a, think)
        t += timedelta(minutes=rng.randint(1, 6))
        if i < len(pairs) - 1 and rng.random() < 0.3:
            c.add("human", t, sprinkle(rng.choice(FOLLOWUPS)))
            t += timedelta(seconds=rng.randint(10, 40))
            c.add("assistant", t, rng.choice(ACKS))
            t += timedelta(minutes=rng.randint(1, 4))
    return c


def checkin_conv(n, title, first_day, days, make):
    c = Conv(n, title)
    day = first_day
    for i in range(days):
        t = cn_time(day, pick_hour(), rng.randrange(60))
        q, a = make(i)
        c.add("human", t, q)
        c.add("assistant", t + timedelta(seconds=rng.randint(15, 60)), a)
        day += timedelta(days=rng.choice([1, 1, 1, 2]))
        if day >= END:
            break
    return c


def words_day(i):
    w = WORDS[i % len(WORDS)]
    return (sprinkle(f"今天的单词：{w}，帮我造个句"),
            f"*{w}* —— 例句：\n\n> She remained {w} throughout the long project.\n\n试着用它说一句关于你今天的话？")


def run_day(i):
    r = RUNS[i % len(RUNS)]
    return (sprinkle(f"打卡：{r}"), rng.choice(["不错，保持节奏！", "很稳，记得拉伸。", "进步明显 🎉", "休息也是训练的一部分。"]))


def main():
    existing = json.loads(OUT.read_text(encoding="utf-8"))
    hand = [c for c in existing if not c["uuid"].startswith("demo-conv-g")]

    convs = []
    n = 1
    keys = list(TOPICS)
    for i in range(44):
        convs.append(topic_conv(n, keys[i % len(keys)], deep=(i % 9 == 4)))
        n += 1
    convs.append(checkin_conv(n, "每日一词打卡", datetime(2025, 11, 3, tzinfo=CN), 50, words_day)); n += 1
    convs.append(checkin_conv(n, "跑步记录", datetime(2026, 1, 5, tzinfo=CN), 34, run_day)); n += 1
    convs.append(checkin_conv(n, "单词打卡 · 第二轮", datetime(2026, 2, 16, tzinfo=CN), 30, words_day)); n += 1

    out = hand + [c.to_json() for c in convs]
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    msgs = sum(len(c["chat_messages"]) for c in out)
    print(f"{len(out)} conversations, {msgs} messages, {OUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
