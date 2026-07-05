// 光影与信仰 — 数据
// 所有摘要为本站基于公开剧情与作者评论切入角度自撰，不复制原文。
// 所有"出处链接"指向合法公开页面（豆瓣图书等）。

const AUTHORS = [
  {
    id: "qihongwei",
    name: "齐宏伟",
    penName: "小约翰",
    born: 1972,
    title: "南京师范大学文学院副教授",
    field: "基督教与中西文学",
    bio: "1972 年生于沂蒙山区，南京大学比较文学专业毕业，笔名小约翰。长期研究基督教与中西文学，著有《信与思》《心有灵犀》《一生必读的关于信仰与人生的 30 部经典》《书中之书讲演录》等。其影评以文学经典评论者的眼光解剖当代电影，主张\"以道观影\"，追问人性与人心真相。",
    works: [
      { title: "牛人看电影·齐宏伟篇", publisher: "华夏出版社", year: 2018, count: 35 },
      { title: "寻找感动力：跟齐宏伟一起看电影", publisher: "", year: 2020, count: 25 }
    ],
    source: "https://book.douban.com/subject/10521792/"
  },
  {
    id: "shihengtan",
    name: "石衡潭",
    penName: "",
    born: null,
    title: "中国社会科学院博士",
    field: "基督教与影视",
    bio: "中国社会科学院博士，曾为美国伯克利大学访问学者。长期透过圣经视角解读中外影视，主张\"掬影视的水，解信仰的渴\"。常在高校与企业做\"影像、青春、爱\"主题讲座，用宗教哲学观点解读电影里的人生。",
    works: [
      { title: "光影中的信望爱", publisher: "世界图书出版公司", year: 2013, count: 40 }
    ],
    source: "https://book.douban.com/subject/25779936/"
  },
  {
    id: "wangshuya",
    name: "王书亚",
    penName: "",
    born: null,
    title: "大学教师，《南方人物周刊》专栏作家",
    field: "信仰与影视",
    bio: "大学教师，曾任《南方人物周刊》\"电光倒影\"专栏作家。其影评\"睿智犀利又充满激情\"，从信仰与人生角度俯瞰几十部经典影片，在罪与恩典、偶像与主权的张力中解读电影。文集附录列有 220 部与信仰有关的电影推荐。",
    works: [
      { title: "天堂沉默了半小时：影视中的信仰与人生", publisher: "江西人民出版社", year: 2008, count: 30 }
    ],
    source: "https://book.douban.com/subject/3009030/"
  },
  {
    id: "liuxiaofeng",
    name: "刘小枫",
    penName: "",
    born: 1956,
    title: "学者，中国人民大学教授",
    field: "中西思想史 / 比较诗学",
    bio: "1956 年生于重庆，学者。代表作《拯救与逍遥》（1988 初版）以比较诗学方式，将中西文化精神概括为\"拯救\"（基督教）与\"逍遥\"（中国儒道）两种路径。虽非影评集，但其对《海上钢琴师》《黑客帝国》等影片的讨论在汉语思想界影响深远，是理解华语基督教文化评论绕不开的坐标。",
    works: [
      { title: "拯救与逍遥（修订版）", publisher: "上海三联书店", year: 2001, count: 0 }
    ],
    source: "https://book.douban.com/subject/2213463/"
  },
  {
    id: "christiantimes",
    name: "基督时报",
    penName: "福音影评",
    born: null,
    title: "中文基督教媒体平台",
    field: "福音影评 / 信仰与文化",
    bio: "基督时报（chinachristiantimes.com）是中文基督教媒体平台，设有\"福音影评\"专栏，刊载多位基督徒作者从信仰视角出发的电影评论，关注信仰、人性、救赎与恩典等主题。作者群包括王新毅、肖朋、沐风等。",
    works: [],
    source: "https://www.chinachristiantimes.com/category/111/%E5%BD%B1%E8%A7%86"
  }
];

// 精选电影（每部附 motif 用于生成 SVG 插画；summary 为本站自撰概括）
const FILMS = [
  {
    id: "haishang-piano",
    title: "海上钢琴师",
    titleEn: "The Legend of 1900",
    year: 1998,
    director: "朱塞佩·托纳多雷",
    country: "意大利",
    genre: "剧情 / 音乐",
    summary: "弃婴\"1900\"一生未下过远洋客轮，以天赋琴艺惊艳世人，最终选择与船同沉。本片追问：当一个人拒绝踏入\"无限\"的世界，是怯懦，还是另一种忠诚？齐宏伟借\"1900 为何不下船\"切入，谈人在有限中的安顿；刘小枫在《拯救与逍遥》的语境中，将\"诗人之死\"读作信仰危机。",
    reviews: [
      { authorId: "qihongwei", work: "《寻找感动力：跟齐宏伟一起看电影》", section: "1900 为什么就是不愿下船", source: "https://book.douban.com/subject/10521792/" },
      { authorId: "liuxiaofeng", work: "《拯救与逍遥》（相关讨论）", section: "", source: "https://book.douban.com/subject/2213463/" }
    ]
  },
  {
    id: "miyang",
    title: "密阳",
    titleEn: "Secret Sunshine",
    year: 2007,
    director: "李沧东",
    country: "韩国",
    genre: "剧情",
    summary: "丧子的母亲申爱在教会里痛哭得安慰，决意去监狱饶恕杀子凶手；却被告知上帝已先她一步赦免了他。她崩溃地质问：\"我还没原谅他，上帝凭什么原谅他？\"",
    reviews: [
      { 
        authorId: "wangshuya", 
        work: "电光倒影专栏 · 南方人物周刊", 
        section: "每一缕阳光都有意思", 
        source: "https://news.sina.cn/sa/2007-11-02/detail-ikftssap2968026.d.html",
        excerpt: "影片在此时陡然转捩，隔着玻璃墙凶手平静地说，感谢上帝，他已赦免了我的罪，我也成了一个基督徒。申爱僵住了，一出监狱，便在阳光下昏厥。她一生的怨恨这才被更深地激发出来。对生命的质疑，不再是'为什么我要遇上这些痛苦'，而是'我还没有原谅他，上帝凭什么原谅他'？平安喜乐回归歇斯底里，申爱怨恨的对象从苦难转向了信仰。她在教堂故意嘶叫，她用'都是假的'的流行乐替换布道大会的赞美诗，她引诱牧师，朝着深夜聚集为她祷告的信徒家里扔石头，直到割腕自杀。"
      },
      { 
        authorId: "shihengtan", 
        work: "豆瓣影评", 
        section: "今生的骄傲", 
        source: "https://m.douban.com/movie/review/2127337",
        excerpt: "《密阳》讲的是一个骄傲被粉碎的故事，包括其怵目惊心之过程与惨不忍睹之后果。李申爱是一个极其骄傲的人。这种骄傲是骨子里的，自然也会通过她的一举手一投足表现出来。骄傲的人就是生活在自己所建构的世界中的人，就是自以为是的人。信仰是什么呢？信仰是固有的颠倒，是习惯的改变，是脱胎换骨，重新做人。接受信仰最大的障碍是什么呢？是自我，是自我中心的观念与意识；而自我中最顽固与最强大的又是什么呢？是人的骄傲。"
      }
    ]
  },
  {
    id: "daomeng",
    title: "盗梦空间",
    titleEn: "Inception",
    year: 2010,
    director: "克里斯托弗·诺兰",
    country: "美国",
    genre: "科幻 / 悬疑",
    summary: "造梦师潜入他人梦境植入念头，现实与梦的边界随一只旋转的陀螺摇晃。齐宏伟问：\"思想是能传染的病毒吗？\"石衡潭则把\"反认他乡是故乡\"读作对永恒家乡的乡愁。",
    reviews: [
      { authorId: "qihongwei", work: "《牛人看电影·齐宏伟篇》", section: "", source: "https://book.douban.com/subject/10521792/" },
      { authorId: "shihengtan", work: "《光影中的信望爱》第五辑 诱惑与希望", section: "反认他乡是故乡", source: "https://book.douban.com/subject/25779936/" }
    ]
  },
  {
    id: "haoke",
    title: "黑客帝国",
    titleEn: "The Matrix",
    year: 1999,
    director: "沃卓斯基姐妹",
    country: "美国",
    genre: "科幻 / 动作",
    summary: "程序员尼奥发现\"现实\"是机器构筑的虚拟牢笼，吞下红色药丸后觉醒。王书亚读出诺斯替主义的创世记；刘小枫在《拯救与逍遥》的框架里，将\"逃离洞穴\"视作拯救与逍遥的现代寓言。",
    reviews: [
      {
        authorId: "wangshuya",
        work: "电光倒影专栏 · 南方人物周刊（收录于《天堂沉默了半小时》）",
        section: "诺斯替主义的创世记",
        source: "http://m.toutiao.com/group/6238977928777154818/",
        excerpt: "几年前，我刚看沃卓斯基兄弟的《骇客帝国》三部曲，只觉它是一个揉合了东方奥秘思想的宇宙论。却没察觉它是古老的诺斯替主义的一个高科技版本。诺斯替主义是公元二、三世纪出现的一种宗教，受东方哲学和基督信仰的双重影响。它的根本思想就是一种极端的二元论……今天所谓的\"现代性\"，其实很大程度上是古代诺斯替主义的复兴。《骇客》电影系列，其实是对圣经《创世记》的一次雄心勃勃的改写。"
      },
      { authorId: "liuxiaofeng", work: "拯救与逍遥（学界讨论）", section: "", source: "https://book.douban.com/subject/2213463/" }
    ]
  },
  {
    id: "yidaizongshi",
    title: "一代宗师",
    titleEn: "The Grandmaster",
    year: 2013,
    director: "王家卫",
    country: "中国 / 香港",
    genre: "剧情 / 武侠",
    summary: "叶问的武林，是\"念念不忘，必有回响\"的执念，也是\"见自己、见天地、见众生\"的修行。齐宏伟追问这\"回响\"最终落向何处；石衡潭借此谈\"何以见自己见众生\"。",
    reviews: [
      { authorId: "qihongwei", work: "《牛人看电影·齐宏伟篇》", section: "", source: "https://book.douban.com/subject/10521792/" },
      { authorId: "shihengtan", work: "《光影中的信望爱》第五辑 诱惑与希望", section: "何以见自己见众生", source: "https://book.douban.com/subject/25779936/" }
    ]
  },
  {
    id: "beican-shijie",
    title: "悲惨世界",
    titleEn: "Les Misérables",
    year: 2012,
    director: "汤姆·霍珀",
    country: "英国 / 美国",
    genre: "剧情 / 歌舞",
    summary: "冉阿让偷银器被主教宽恕后重生，一生在律法与恩典之间挣扎。沙威恪守律法终至自毁。石衡潭读出\"真正的革命是爱与饶恕\"——福音比革命更彻底。",
    reviews: [
      { authorId: "shihengtan", work: "《光影中的信望爱》第六辑 爱与饶恕", section: "真正的革命是爱与饶恕", source: "https://book.douban.com/subject/25779936/" }
    ]
  },
  {
    id: "tangshan-dizhen",
    title: "唐山大地震",
    titleEn: "Aftershock",
    year: 2010,
    director: "冯小刚",
    country: "中国",
    genre: "剧情",
    summary: "一位母亲在废墟中只能救一个孩子，她选了弟弟。三十二年后，幸存的女儿归来。石衡潭问：\"在哪里等候你，我的亲人？\"——苦难中的等候与悔改还是遗忘之间的抉择。",
    reviews: [
      { authorId: "shihengtan", work: "《光影中的信望爱》第四辑 痛苦与救赎", section: "在哪里等候你？我的亲人！", source: "https://book.douban.com/subject/25779936/" }
    ]
  },
  {
    id: "jianyuzhe",
    title: "窃听风暴",
    titleEn: "The Lives of Others",
    year: 2006,
    director: "弗洛里安·亨克尔·冯·多纳斯马克",
    country: "德国",
    genre: "剧情 / 惊悚",
    summary: "斯塔西特工奉命监听一位剧作家，却在倾听中被人性的温度改变，暗中保护了他。王书亚读出\"我们头顶干净的天空\"——恩典如何在最冰冷的地方临到。",
    reviews: [
      { authorId: "wangshuya", work: "《天堂沉默了半小时》第一辑 罪", section: "我们头顶干净的天空", source: "https://book.douban.com/subject/3009030/" }
    ]
  },
  {
    id: "qiyi-enedian",
    title: "奇异恩典",
    titleEn: "Amazing Grace",
    year: 2006,
    director: "迈克尔·艾普特",
    country: "英国 / 美国",
    genre: "剧情 / 传记",
    summary: "威廉·威伯福斯以一生推动英国废除奴隶贸易，靠的不是革命，而是信念与议会里的持久争战。王书亚读出\"少一个奴隶，多一个弟兄\"；齐宏伟则谈\"以信念改变世界\"。",
    reviews: [
      { authorId: "wangshuya", work: "《天堂沉默了半小时》第三辑 爱", section: "少一个奴隶，多一个弟兄", source: "https://book.douban.com/subject/3009030/" },
      { authorId: "qihongwei", work: "《牛人看电影·齐宏伟篇》", section: "以信念改变世界", source: "https://book.douban.com/subject/10521792/" }
    ]
  },
  {
    id: "zhao-shi-guer",
    title: "赵氏孤儿",
    titleEn: "Sacrifice",
    year: 2010,
    director: "陈凯歌",
    country: "中国",
    genre: "剧情 / 历史",
    summary: "为复仇献出亲子，又以仇人之子为养子。当真相揭晓，复仇的刀刃指向的是自己一手养大的孩子。石衡潭与王书亚都借此追问：\"为什么我们爱不起来？\"——仇恨如何吞噬爱的能力。",
    reviews: [
      { authorId: "shihengtan", work: "《光影中的信望爱》第六辑 爱与饶恕", section: "为什么我们爱不起来？", source: "https://book.douban.com/subject/25779936/" },
      { authorId: "wangshuya", work: "《天堂沉默了半小时》（相关讨论）", section: "", source: "https://book.douban.com/subject/3009030/" }
    ]
  },
  {
    id: "shenhe",
    title: "深河",
    titleEn: "Deep River",
    year: 1995,
    director: "熊井启",
    country: "日本",
    genre: "剧情",
    summary: "改编自远藤周作同名小说。一群日本人来到印度恒河边，各自带着不同的困惑与执念。美津子曾戏弄基督徒同学大津，多年后在加尔各答遇见成为神父的他。王书亚借远藤周作的叙事，读出\"软弱中的信心\"与\"真实的基督徒\"——德兰修女日记揭示的\"灵里贫乏\"，恰是大津形象的写照。",
    reviews: [
      {
        authorId: "wangshuya",
        work: "电光倒影专栏 · 南方人物周刊",
        section: "我也是其中的一部分",
        source: "https://news.sina.cn/sa/2008-08-12/detail-ikftpnny4046738.d.html",
        excerpt: "在《深河》中，人们也怀抱各种信念，聚集在恒河边。美津子和那位梦想在恒河蝶泳的女孩颇为类似，甚至更为后现代。她挑逗基督徒同学大津，如果大津愿意放弃信仰，她就爱他，把大津耍得团团转。多年后，一无所信的美津子在婚姻中无望，转眼仰望恒河和印度的神祇们，结果在加尔各答遇见了成为神父的大津。远藤在多元宗教的现代场景中，塑造了一个现代的灵魂，美津子；和一个古旧的灵魂，大津。"
      }
    ]
  },
  {
    id: "threehundred",
    title: "300",
    titleEn: "300",
    year: 2006,
    director: "扎克·施奈德",
    country: "美国",
    genre: "动作 / 战争",
    summary: "温泉关之战，斯巴达三百勇士对抗波斯十万大军。王书亚读出\"国家只能是一条狗\"——柏拉图的哲学狗，对外凶狠对内温柔。当列奥尼达喊出\"自由\"，背后是先对自己公民\"秋风扫落叶\"的残酷。波斯与斯巴达，民主与君主，都将虚妄的主权看作绝对偶像。",
    reviews: [
      {
        authorId: "wangshuya",
        work: "电光倒影专栏 · 南方人物周刊",
        section: "国家只能是一条狗",
        source: "https://news.sina.cn/sa/2007-04-24/detail-ikftpnny3857792.d.html",
        excerpt: "看到影片中每个被扔进山谷的婴孩，每个在丛林原则下被一路淘汰的斯巴达人，你又发现原来\"以少胜多\"只是假象。什么样的社会才能煅炼出抗击10万大军的300勇士？敌人没来之前，就去芜存菁，先把自己的孩子杀掉一半。你恍然大悟，这是人海战术的另外一种。波斯是把百姓开到战场上当炮灰；斯巴达呢，是上场之前就把这个问题解决了。"
      }
    ]
  },
  {
    id: "blood",
    title: "血色将至",
    titleEn: "There Will Be Blood",
    year: 2007,
    director: "保罗·托马斯·安德森",
    country: "美国",
    genre: "剧情",
    summary: "石油大亨丹尼尔·普莱恩维尤从孤零淘金者到冷酷大亨，一生在石油与信仰之间挣扎。传教士伊莱以\"圣灵充满\"为名行贪婪之实。王书亚读出\"石油与圣灵\"的双重堕落——石油是丹尼尔的宗教，圣灵是伊莱的石油。片名出自《出埃及记》：耶和华审判埃及，水变成血。",
    reviews: [
      {
        authorId: "wangshuya",
        work: "电光倒影专栏 · 南方人物周刊",
        section: "路上行人欲断魂",
        source: "https://news.sina.cn/sa/2008-04-17/detail-ikftpnny4007160.d.html",
        excerpt: "石油大亨丹尼尔，在空旷的豪宅，不能遏止一生的血气，用保龄球瓶杀死了伊莱，这个在灵魂的油田上和他一样野心勃发的传教士。他坐在地上说出全片最后一句台词，\"我结束了。\"影片将丹尼尔的\"石油\"和伊莱的\"圣灵充满\"——这德州贡献给美国的两大财富——并列在了一起。对丹尼尔来说，石油是他的宗教；对伊莱来说，\"圣灵\"就是他的石油。"
      }
    ]
  },
  {
    id: "tiangou",
    title: "天狗",
    titleEn: "The Forest Ranger",
    year: 2006,
    director: "戚健",
    country: "中国",
    genre: "剧情",
    summary: "战斗英雄李天狗退役后成为护林员，守护国有林却遭全村孤立。孔家三兄弟为砍树致富用尽手段，天狗以血肉之躯对抗黑恶势力。石衡潭追问：\"还有比国家利益更高的目标吗？\"——当所有人都为利益而来，谁来守护那片林子？谁来守护正义？",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "还有比国家利益更高的目标吗？",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20121002",
        excerpt: "影片中各种矛盾和冲突都是围绕林子展开的。这是一片在干旱的山区极其珍贵的国有林。它是国家的财产，可因它地处泮源村，也成为村里人眼馋的宝贝，更是孔家三兄弟致富的源头。而李天狗是一个退役的老兵，他的薪水是来自政府，他的任务是看护林子。村民与他的关系是吃林的人与护林的人的关系。吃林的人与护林的人的利益，立场与目标是截然相反的，他们之间自然会有矛盾。"
      }
    ]
  },
  {
    id: "shuxiansheng",
    title: "Hello！树先生",
    titleEn: "Mr. Tree",
    year: 2011,
    director: "韩杰",
    country: "中国",
    genre: "剧情",
    summary: "树先生是底层人中的底层人，任人摆布，可有可无。父亲失手勒死哥哥的阴影始终缠绕着他。他张开双臂像一棵树，等待有人牵他的手。石衡潭读出\"谁牵我手\"——暴力如何代代相传，爱如何缺席。树的手既是渴望，也是无力。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "谁牵我手？",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20120202",
        excerpt: "树不只是一个底层人，边缘人，而且是一个底层人中的底层人，边缘人中的边缘人。就是在自己的环境中，他也是一个任人摆佈，可有可无的人。人高兴的时候，可以赏他喝一顿酒，也可以让他在別人婚礼上讲两句话；不高兴的时候，可以命他在別人婚礼上下跪，连弟弟也会在他结婚前夜狠狠揍他。"
      }
    ]
  },
  {
    id: "fengkuang-shitou",
    title: "疯狂的石头",
    titleEn: "Crazy Stone",
    year: 2006,
    director: "宁浩",
    country: "中国",
    genre: "喜剧",
    summary: "一块价值连城的翡翠引发几方人马的疯狂争夺。保安、小偷、国际大盗，白天是邻居，夜晚是对手。石衡潭读出\"卿为何狂\"——敬虔加上知足的心便是大利，但那些想要发财的人就陷在迷惑。疯狂之后，石头还是石头，人却已不再是人。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "卿为何狂？",
        source: "https://chs.ebaomonthly.com/ebao/readebao.php?a=20120701",
        excerpt: "这个片名很奇怪，石头怎么能疯狂呢？看完这部影片，才觉得这个片名还是有其妙处，可以说是对这个时代的一种富有深意的嘲讽。故事是围绕石头展开的，疯狂也是因一块石头而起，只不过人们将这块石头叫作翡翠罢了。石头其实是不会疯狂的，但在这个疯狂的时代，可能它也在所难免。只是，人们在经历了那样的疯狂之后，许多已经不再是人了；而石头见证了人们的疯狂之后，依然是一块石头。"
      }
    ]
  },
  {
    id: "zhiqingchun",
    title: "致我们终将逝去的青春",
    titleEn: "So Young",
    year: 2013,
    director: "赵薇",
    country: "中国",
    genre: "剧情 / 爱情",
    summary: "郑微从敢爱敢恨到学会放手，陈孝正以\"一厘米人生\"哲学抛弃爱情。石衡潭读出\"爱自己胜过爱爱情\"——林静的狭隘、赵世永的懦弱、陈孝正的自私，每个人都最爱自己。青春就是用来怀念的，但怀念什么？",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "爱自己？爱爱情？还是爱…",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20130903",
        excerpt: "应该说：人人都最爱自己，或者说人人都是自私的，只是表现方式有別而已。对於林靜来说，他的自私表现在狭隘。知道了父亲与郑微母亲的姦情后，他心中的道德丰碑轰然倒塌，随后，他不仅疏远了父亲，连与郑微这份情感也毅然断绝了。陈孝正是这些男生中最优秀的，也是最有责任感的，可恰恰又是最自私的。这种自私是骨子里的，不到一定时刻还显现不出来。这就是他的\"一釐米\"人生哲学：\"我的人生是一栋只能建造一次的大楼，我必须让它精确无比，不能有一釐米差池。\""
      }
    ]
  },
  {
    id: "chepiao",
    title: "车票",
    titleEn: "Ticket",
    year: 2008,
    director: "张之亮",
    country: "中国",
    genre: "剧情",
    summary: "孤儿雨桐在养母去世后，凭借两张旧车票踏上寻亲之路。母亲每年千里迢迢去看她，却从不让她知道。石衡潭读出\"爱是永不止息\"——母爱是舍棄，也是坚持。寻找的过程就是了解与理解的过程，也是原谅与接纳的过程。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "爱是永不止息",
        source: "http://chs.ebaomonthly.com/ebao/printebao.php?a=20091006",
        excerpt: "雨桐是一个被遗棄的孤儿，幸运的是，她被善良的修女曾嬤嬤抱养带大，並且有了令人羡慕的生活与事业。多少年来，她一直把嬤嬤当作了自己的母亲，而怨恨那两个遗棄了自己的人。可是，生活並非总是依照人的意愿走，甚至常常跟人对着干。嬤嬤的突然去世与她所留下的两张旧车票都给她提出了一个迫切的任务：寻根，寻找自己的生身父母。"
      }
    ]
  },
  {
    id: "qianli-zou-danqi",
    title: "千里走单骑",
    titleEn: "Riding Alone for Thousands of Miles",
    year: 2005,
    director: "张艺谋",
    country: "中国",
    genre: "剧情",
    summary: "日本老人高田健一与儿子隔膜多年，儿子重病后他来到中国丽江，只为完成儿子的一个心愿——拍摄傩戏《千里走单骑》。石衡潭读出\"拿什么奉献给你\"——父子间的隔阂与和解，传统与现代的碰撞，沟通的艰难与可能。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "拿什么奉献给你",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20120901",
        excerpt: "\"千里走单骑\"是一个我们所熟悉的关於关公的故事，它表现的是传统中国人重然诺，轻富贵，讲义气，报恩情的精神。这样一种精神，对於今天的中国人来说，已经非常陌生了。张艺谋把它从传统深处打捞出来，是何用意呢？是要喚起人们对传统的关注？还是想让人们深入眼前的现实呢？我看是兼而有之。传统並沒有真正死去，而是或隐或显地存於我们的现实之中，当我们潛沉到现实的深处，就会遭遇那古老的传统。"
      }
    ]
  },
  {
    id: "sousuo",
    title: "搜索",
    titleEn: "Caught in the Web",
    year: 2012,
    director: "陈凯歌",
    country: "中国",
    genre: "剧情 / 悬疑",
    summary: "叶蓝秋在公交车上不让座，一段视频引发网络风暴，最终走向绝望。石衡潭追问\"真相是什么？\"——网络时代人人都在搜索真相，可真相未必是人们想要看到的。在大众狂欢般的搜索中，各人又露出了各自的真相。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "真相是什么？",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20121101",
        excerpt: "一件事情发生了，人人都急於知道真相。在传统社会，通讯不便，人们可能很难得到真正有用的信息，而在网络时代，无数扑面而来的资讯，同样让你无所适从，找不着北。以前人们常说，耳听为虛，眼见为实。可是在今天，看到的也不一定就是真相。其实，人们想要搜索的也不一定是真相，而是想要看到自己所想要看到的，还有一些人是想要达到自己所想要达到的。真相並不重要，重要的是各人的心思意念。"
      }
    ]
  },
  {
    id: "yuntu",
    title: "云图",
    titleEn: "Cloud Atlas",
    year: 2012,
    director: "沃卓斯基姐妹 / 汤姆·提克威",
    country: "美国 / 德国",
    genre: "科幻 / 剧情",
    summary: "六个时空交错的故事，从19世纪的南太平洋到末日后的夏威夷，每一个选择都在影响未来。石衡潭评价：\"没有众多水滴，又哪来汪洋？\"——影片以佛教六道轮回结构剧情，但生命的宝贵正在于一次性，不可逆转的抉择才真正有意义。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "没有众多水滴，又哪来汪洋？",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20130501",
        excerpt: "本片改编自大卫．米切尔的同名小说Cloud Atlas。编导以佛教的六道轮回观念来结构剧情，展开了在六个时空中的故事，它们之间既彼此独立，各自发展，又有着某种內在相似，甚至以某种标记来关联。影片強调了人类的互相依存，行善決定的重要性。这是值得肯定的。但应该说，生命沒有轮回，生命的宝贵就在於一次性。如果有轮回，我们会把善的抉择总是留给下一次，而不去做现实的承担。只有在仅有一次的生命中，作出那至关重要且不可更改的抉择，才是意义非凡的。"
      }
    ]
  },
  {
    id: "zhi-qing-chun",
    title: "致我们终将逝去的青春",
    titleEn: "So Young",
    year: 2013,
    director: "赵薇",
    country: "中国",
    genre: "剧情 / 爱情",
    summary: "大学时代的爱情与迷茫，郑微、陈孝正、阮莞……每个人的青春都有遗憾。石衡潭追问：\"爱自己？爱爱情？还是爱…\"——人人都最爱自己，可爱情的真义是舍己。没有信仰的青春，终究只是一场怀念。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "爱自己？爱爱情？还是爱…",
        source: "https://chs.ebaomonthly.com/ebao/printebao.php?a=20130903",
        excerpt: "致我们终将逝去的青春上映以来，十分火爆，不到一週，票房已超过三亿，更是出现一边倒的好评如潮。这里有青春的单纯，率真，激情，奔放，也有青春的鲁莽，迷茫，错误，悲伤。青春最重要最动人心弦的主题还是爱情。尽管影片中每个人的爱情际遇与归宿各不相同，而女主人公郑微后来则一言以概之：\"我们都应该惭愧，我们都爱自己胜过爱爱情。\"这可以说是全片的点睛之笔，也是编导品评人物的标准尺度。"
      }
    ]
  },
  {
    id: "amish-grace",
    title: "阿米什的恩典",
    titleEn: "Amish Grace",
    year: 2010,
    director: "格雷格·钱皮恩",
    country: "美国",
    genre: "剧情",
    summary: "真实事件改编：阿米什学校枪击案后，阿米什社区选择饶恕凶手。石衡潭探讨「愿你饶恕我们的亏欠」——什么是饶恕？饶恕如何可能？从信仰的角度，揭示饶恕的真谛与力量来源。",
    reviews: [
      {
        authorId: "shihengtan",
        work: "翼报 · 艺文走廊",
        section: "愿你饶恕我们的亏欠",
        source: "https://chs.ebaomonthly.com/ebao/readebao.php?a=20120401",
        excerpt: "什么是饶恕？饶恕如何可能？什么人什么罪可以饶恕？难道杀人犯杀人罪也可以饶恕吗？案件爆发的当天，阿米什长老就带着包括受难者玛丽贝斯的父亲吉迪恩在內的二人代表阿米什社区去探望肇事者的妻子与父亲。吉迪恩说：\"你失去了丈夫，孩子们失去了父亲，我们也为你哀悼。\"长老接着说：\"我们过来告诉你我们饶恕他。\"长老说：\"你们饶恕人的过犯，你们的天父也必饶恕你们的过犯。\"此语出自於圣经马太福音6:14，它揭示了饶恕的真谛，也指出了人饶恕力量的来源。"
      }
    ]
  },
  {
    id: "muqin",
    title: "母亲",
    titleEn: "Kabei: Our Mother",
    year: 2008,
    director: "山田洋次",
    country: "日本",
    genre: "剧情 / 家庭",
    summary: "二战时期，丈夫野上因反战言论被捕入狱死在狱中，妻子独自抚养两个女儿，一生在天皇崇拜与信仰之间挣扎。王书亚读出「给父亲的安魂曲」——母亲临终遗言\"我不要来世，我要今生见到活着的丈夫\"，原来被拿走的，不只是今生，还有永恒的盼望。",
    reviews: [
      {
        authorId: "wangshuya",
        work: "电光倒影专栏 · 南方人物周刊",
        section: "给父亲的安魂曲",
        source: "http://news.sohu.com/20080828/n259252330.shtml",
        excerpt: "母亲弥留之际，小女儿照美在床头安慰母亲，说\"妈妈，你就会见到爸爸了\"。这位含辛茹苦的母亲，撑着说出最后的遗言，\"我不要来世，我要今生见到活着的丈夫。\"堆积了两个小时的情感，在最后一秒爆发。照美嚎啕大哭起来，因为母亲忍耐了一生，却死不甘心。因为半个世纪前被剥夺的，半个世纪后依然如此锥心。原来被拿走的，不只是今生，还有永恒的盼望。"
      }
    ]
  },
  {
    id: "xuezhan-gangyaoling",
    title: "血战钢锯岭",
    titleEn: "Hacksaw Ridge",
    year: 2016,
    director: "梅尔·吉布森",
    country: "美国 / 澳大利亚",
    genre: "剧情 / 战争 / 传记",
    summary: "真实故事改编：基督复临安息日会信徒戴斯蒙德·道斯拒绝携带武器上战场，作为军医在冲绳战役中赤手空拳救下75位战友。基督时报评论：信仰的力量坚不可摧——\"不可杀人\"的诫命在他脑海里深深种下，他以不杀的方式报国。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 福音影评",
        section: "信仰是证明我活着",
        source: "https://www.chinachristiantimes.com/news/22519/",
        excerpt: "他从来没有想到自己有一天会受到美国前后二任总统的接见并颁发勋章，成为国家民族的大英雄。更没想到他的故事在死后还拍成了电影，这一切都是因为他持守了自己的信仰，坚不可摧，从未动摇！道斯坚持宗教信仰是他的力量之源，坚恪守上帝的准则，任何时候都不可违背，即使在战争中面对要杀死他的仇敌，不可杀人还是不可杀人。"
      }
    ]
  },
  {
    id: "huoxing-jiuyuan",
    title: "火星救援",
    titleEn: "The Martian",
    year: 2015,
    director: "雷德利·斯科特",
    country: "美国",
    genre: "科幻 / 冒险 / 剧情",
    summary: "宇航员马克被遗留在火星上，独自求生。地球上的同伴们不惜一切代价也要带他回家。基督时报王新毅从\"浪子的比喻\"切入——一个人的灵魂比宇宙都更宝贵，上帝的算术是1>99。耶稣从天堂来到人间，为拯救我们所有人回家。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 福音影评",
        section: "《火星救援》与耶稣讲的「浪子的比喻」有何异同？",
        source: "https://www.chinachristiantimes.com/news/19814/",
        excerpt: "为救一个人回家，人类数百数千亿美金的设备都不过是随意拆卸的工具。这是关乎生命的真理。基督教教给我们的是：一个人的灵魂比宇宙都更宝贵。圣经路加福音中\"浪子的比喻\"中耶稣告诉我们，在上帝眼中那1只迷羊是比99只在圈里的羊更为宝贵的，这是上帝的算术：1>99，因为生命不是按照数字来计算的。因此，耶稣从天堂来到人间。《火星救援》中是所有人努力让马克从另外一个星球回来，而福音让我们看到的是：耶稣为了拯救我们，他一个人来到我们的星球拯救我们所有人回家。"
      }
    ]
  },
  {
    id: "mogui-daiyanren",
    title: "魔鬼代言人",
    titleEn: "The Devil's Advocate",
    year: 1997,
    director: "泰勒·海克福德",
    country: "美国",
    genre: "剧情 / 悬疑 / 恐怖",
    summary: "不败律师凯文在名利与正义之间一步步沦陷。他的老板米尔顿，其实是魔鬼的父亲。肖朋从基督时报评论：\"要用一生对抗虚荣\"——魔鬼最爱的原罪就是虚荣。每一个选择，都是我们自己做出的。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 福音影评",
        section: "要用一生对抗虚荣",
        source: "https://chinachristiantimes.com/news/40239/",
        excerpt: "律师的职责本来是伸张正义，为无罪的伸冤辩屈，凯文却发现自己所作的辩护纯粹是为了金钱、名誉和众人的喝彩。只要可以满足自己的虚荣，至于案情真相如何，委托人究竟有罪无罪，倒成为无关紧要，甚至可以成为任意颠倒的了。当凯文看清魔鬼的身份，将一切责任推卸到魔鬼身上的时候，魔鬼却提醒他说：\"我并不是一个操纵者，我没有让事情发生。不要忘了，做出选择的是你自己。\""
      }
    ]
  },
  {
    id: "xiaoluoli-houshen-dashu",
    title: "小萝莉的猴神大叔",
    titleEn: "Bajrangi Bhaijaan",
    year: 2015,
    director: "卡比尔·汗",
    country: "印度",
    genre: "剧情 / 喜剧 / 冒险",
    summary: "巴基斯坦哑女在印度与母亲失联，印度教信徒帕万不顾两国敌对，跨越宗教与国界送她回家。基督时报沐风评论：\"跨越内心的障碍，方能换来人性中的纯与善\"——人与人的最大障碍不是国界、宗教、文化，而是心的距离。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 福音影评",
        section: "跨越内心的障碍，方能换来人性中的纯与善",
        source: "https://www.chinachristiantimes.com/news/40702/",
        excerpt: "\"回家\"的这一观念不再是去到指定的一个地方，而是心灵的一个安稳，这需要跨越心灵的障碍，突破固有思想，走出那些限制自己的框架，活出最真实、最善良、最单纯的自己。这部影片最打动人的地方想必就是\"人性中本能的善意最终战胜了头脑中的狭隘与恶毒\"。人与人之间最大的障碍不是国界、宗教、文化，而是人与人之间心的距离。透过爱去分享，去传递，即使遍体鳞伤也是值得的。"
      }
    ]
  },
  {
    id: "nezha2",
    title: "哪吒2",
    titleEn: "Ne Zha 2",
    year: 2025,
    director: "饺子",
    country: "中国",
    genre: "动画 / 奇幻",
    summary: "哪吒被封印后获得新身体，对抗命运的不公。当哪吒喊出\"我命由我不由天\"时，全场为之动容。基督时报肖朋思考：这句话传达的是\"个人主义\"和\"自我救赎\"，但人心筹算自己的道路，惟耶和华指引他的脚步。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 福音影评",
        section: "关于「我命由我不由天」的思考",
        source: "https://www.chinachristiantimes.com/news/42909/",
        excerpt: "我认为\"我命由我不由天\"这句话传达的是一种强烈的\"个人主义\"和\"自我救赎\"的观念。它强调的是个人的力量和意志，认为人可以通过自己的努力来改变命运，摆脱束缚。然而，这种观念也容易让人陷入一种\"自我中心\"的误区。当人们过于强调个人的力量时，便会忽视上帝的主权和恩典。正如所罗门曾告诫他的众子说：\"人心筹算自己的道路，惟耶和华指引他的脚步。\"这表明，尽管人可以有自己的计划和努力，但最终的引导和决定权在上帝手中。"
      }
    ]
  },
  {
    id: "mosha",
    title: "默杀",
    titleEn: "A Place Called Silence",
    year: 2024,
    director: "柯汶利",
    country: "中国",
    genre: "剧情 / 悬疑 / 犯罪",
    summary: "女子中学的校园霸凌引发连环复仇。校长的贿赂、老师的包庇、家长的冷漠、同学的冷眼旁观——集体的沉默也是一种\"杀\"。基督时报絮语评论：基督徒对罪恶不能容忍、不能畏惧、不能麻木。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 影评",
        section: "集体的沉默会「杀」人",
        source: "https://www.chinachristiantimes.com/news/42449/",
        excerpt: "基督徒要学会做自己应该做的事。在名利面前，我们不应该追求，要学会看淡；但面对罪恶时，我们不能依旧看淡，这是一件非常重要的事，应当与它保持远远的距离。不仅自己要离罪，在看到身边同工和弟兄姊妹有罪恶的事后也不要置若罔闻，这是我们的职责，也是我们应尽的义务。当我们对他们犯罪沉默的时候，也是在为自己积攒罪恶。一旦我们对罪恶视而不见，久而久之，就失去了对罪恶的敏感程度。一旦失去了这样的敏感程度，也就真的对罪恶麻木了。"
      }
    ]
  },
  {
    id: "diershitiao",
    title: "第二十条",
    titleEn: "Article 20",
    year: 2024,
    director: "张艺谋",
    country: "中国",
    genre: "剧情 / 喜剧",
    summary: "围绕正当防卫\"第二十条\"展开的三个案件：王永强杀村霸、公交司机见义勇为反被判刑、检察官的儿子见义勇为反被立案。基督时报沐风评论：当该有的公义扭曲时，依然选择相信上帝，等候上帝。",
    reviews: [
      {
        authorId: "christiantimes",
        work: "基督时报 · 影评",
        section: "思考人情社会中是否有公义？",
        source: "https://www.chinachristiantimes.com/news/40973/",
        excerpt: "从信仰的角度谈这部电影的话笔者最大的收获就是\"当该有的公义扭曲时，依然选择相信上帝，等候上帝，因为这是作为基督徒唯一且正确的选择。\"社会上的知识、学历和文凭虽然不能与智慧、能力和水平划上等号，却往往也与我们每一个人都息息相关。基督徒若有了这些常识基础，然后再加上特殊恩典的临到，我们就能够更好的为祂所用，成为祂的美好的见证。"
      }
    ]
  }
];

if (typeof window !== "undefined") {
  window.AUTHORS = AUTHORS;
  window.FILMS = FILMS;
}
