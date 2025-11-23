// 翻譯文件
export const translations = {
  'zh-TW': {
    // Hero Section
    heroTitle: '魷魚遊戲!',
    heroDescription: '這是一個基於機器學習與 SDGs14 製作的破關小遊戲，我們希望同學們與小朋友們能夠真正地從機器學習的角度認識 AI，與此同時，去認識到海洋垃圾對於環境的危害。',
    learnMore: '了解更多',
    viewSource: '查看原始碼',
    
    // About Section
    about: '關於',
    aboutDescription: '這是一個基於機器學習與 SDGs14 製作的破關小遊戲，我們希望同學們與小朋友們能夠真正地從機器學習的角度認識 AI，與此同時，去認識到海洋垃圾對於環境的危害。',
    
    // Contributor Section
    contributor: '作者',
    contributorName: '陳維竣',
    contributorEducation: '教育背景 : 國立政治大學 統計學系學士班',
    
    // Technical Skills Section
    technicalSkills: '用到的技術',
    frontend: '前端',
    backend: '後端',
    aiRelated: 'AI相關',
    tools: '工具',
    
    // Contact Section
    contact: '聯絡我們',
    contactInformation: '聯絡資訊',
    email: '電子郵件',
    homepage: '個人網站',
    location: '所在地',
    locationValue: '臺北, 臺灣',
    
    // Navigation
    navHome: '首頁',
    navEnvironment: '環境安裝',
    navManual: '手動操控',
    navCollect: '收集資料',
    navTrain: '訓練模型',
    navKNN: '使用模型',
    navTemplate: '自定義模板',
    navSpeed: '加速遊戲',
    navContact: '聯絡資訊',
    
    // Sections
    sectionEnvironment: '環境安裝',
    gitInstallTitle: '1️⃣ 安裝 Git',
    gitInstallDesc: '到官方網站下載並安裝（一路按 Next 即可）：',
    gitInstallLink: 'https://git-scm.com/',
    gitInstallCheck: '安裝後開啟終端機輸入：',
    gitInstallCommand: 'git --version',
    gitInstallSuccess: '若有版本號表示安裝成功。',
    gitCloneTitle: '2️⃣ 找到你要下載的 GitHub 專案',
    gitCloneExample: '例如本遊戲專案：',
    gitCloneSteps: '按 Code → HTTPS → Copy 複製連結。',
    gitCloneFolderTitle: '3️⃣ 開啟一個放專案的資料夾',
    gitCloneFolderExample: '例如：',
    gitCloneFolderPath: 'C:\\Users\\你的名字\\Projects',
    gitCloneFolderAction: '在此資料夾按右鍵 → Open in Terminal。',
    gitCloneCommandTitle: '4️⃣ 執行 git clone',
    gitCloneCommandDesc: '在終端機貼上以下指令：',
    gitCloneCommand: 'git clone <剛剛複製的網址>',
    gitCloneCommandExample: '例如：',
    gitCloneResult: '執行後你會在資料夾看到：',
    sectionManual: '手動操控魷魚',
    manualDesc: '於專案目錄下執行：',
    manualCommand: 'python -m mlgame -i .\\ml\\ml_play_manual.py ./ --level 1',
    sectionCollect: '收集魷魚移動資料',
    collectDesc: '於專案目錄下執行：',
    collectCommand: 'python -m mlgame -i .\\ml\\ml_play_collect_data.py ./ --level 1',
    sectionTrain: '訓練 KNN 模型',
    trainDesc: '於專案目錄下執行：',
    trainCommand: 'python .\\ml\\knn_train.py',
    sectionKNN: '使用 KNN 模型操控魷魚',
    knnDesc: '於專案目錄下執行：',
    knnCommand: 'python -m mlgame -i .\\ml\\ml_play_knn.py ./ --level 1',
    sectionTemplate: '執行自定義模板',
    templateDesc: '於專案目錄下執行：',
    templateCommand: 'python -m mlgame -i .\\ml\\ml_play_template.py ./ --level 1',
    sectionSpeed: '加速遊戲',
    speedDesc: '於專案目錄下執行：',
    speedCommand: 'python -m mlgame -f 120 -i .\\ml\\ml_play_knn.py ./ --level 1',
    speedNote: '-f 為設定 fps 的參數，數值越大，fps 越高。',
    
    // Footer
    footer: '© 2025 Wei-Jun Chen · Built with Next.js & shadcn/ui',
  },
  'zh-CN': {
    // Hero Section
    heroTitle: '鱿鱼游戏!',
    heroDescription: '这是一个基于机器学习与 SDGs14 制作的破关小游戏，我们希望同学们与小朋友们能够真正地从机器学习的角度认识 AI，与此同时，去认识到海洋垃圾对于环境的危害。',
    learnMore: '了解更多',
    viewSource: '查看源代码',
    
    // About Section
    about: '关于',
    aboutDescription: '这是一个基于机器学习与 SDGs14 制作的破关小游戏，我们希望同学们与小朋友们能够真正地从机器学习的角度认识 AI，与此同时，去认识到海洋垃圾对于环境的危害。',
    
    // Contributor Section
    contributor: '作者',
    contributorName: '陈维竣',
    contributorEducation: '教育背景 : 国立政治大学 统计学系学士班',
    
    // Technical Skills Section
    technicalSkills: '用到的技术',
    frontend: '前端',
    backend: '后端',
    aiRelated: 'AI相关',
    tools: '工具',
    
    // Contact Section
    contact: '联系我们',
    contactInformation: '联络资讯',
    email: '电子邮件',
    homepage: '个人网站',
    location: '所在地',
    locationValue: '台北, 台湾',
    
    // Navigation
    navHome: '首页',
    navEnvironment: '环境安装',
    navManual: '手动操控',
    navCollect: '收集资料',
    navTrain: '训练模型',
    navKNN: '使用模型',
    navTemplate: '自定义模板',
    navSpeed: '加速游戏',
    navContact: '联络资讯',
    
    // Sections
    sectionEnvironment: '环境安装',
    gitInstallTitle: '1️⃣ 安装 Git',
    gitInstallDesc: '到官方网站下载并安装（一路按 Next 即可）：',
    gitInstallLink: 'https://git-scm.com/',
    gitInstallCheck: '安装后开启终端机输入：',
    gitInstallCommand: 'git --version',
    gitInstallSuccess: '若有版本号表示安装成功。',
    gitCloneTitle: '2️⃣ 找到你要下载的 GitHub 项目',
    gitCloneExample: '例如本游戏项目：',
    gitCloneSteps: '按 Code → HTTPS → Copy 复制连结。',
    gitCloneFolderTitle: '3️⃣ 开启一个放项目的资料夹',
    gitCloneFolderExample: '例如：',
    gitCloneFolderPath: 'C:\\Users\\你的名字\\Projects',
    gitCloneFolderAction: '在此资料夹按右键 → Open in Terminal。',
    gitCloneCommandTitle: '4️⃣ 执行 git clone',
    gitCloneCommandDesc: '在终端机贴上以下指令：',
    gitCloneCommand: 'git clone <刚刚复制的网址>',
    gitCloneCommandExample: '例如：',
    gitCloneResult: '执行后你会在资料夹看到：',
    sectionManual: '手动操控鱿鱼',
    manualDesc: '于专案目录下执行：',
    manualCommand: 'python -m mlgame -i .\\ml\\ml_play_manual.py ./ --level 1',
    sectionCollect: '收集鱿鱼移动资料',
    collectDesc: '于专案目录下执行：',
    collectCommand: 'python -m mlgame -i .\\ml\\ml_play_collect_data.py ./ --level 1',
    sectionTrain: '训练 KNN 模型',
    trainDesc: '于专案目录下执行：',
    trainCommand: 'python .\\ml\\knn_train.py',
    sectionKNN: '使用 KNN 模型操控鱿鱼',
    knnDesc: '于专案目录下执行：',
    knnCommand: 'python -m mlgame -i .\\ml\\ml_play_knn.py ./ --level 1',
    sectionTemplate: '执行自定义模板',
    templateDesc: '于专案目录下执行：',
    templateCommand: 'python -m mlgame -i .\\ml\\ml_play_template.py ./ --level 1',
    sectionSpeed: '加速游戏',
    speedDesc: '于专案目录下执行：',
    speedCommand: 'python -m mlgame -f 120 -i .\\ml\\ml_play_knn.py ./ --level 1',
    speedNote: '-f 为设定 fps 的参数，数值越大，fps 越高。',
    
    // Footer
    footer: '© 2025 Wei-Jun Chen · Built with Next.js & shadcn/ui',
  },
  'en': {
    // Hero Section
    heroTitle: 'Swimming Squid Game!',
    heroDescription: 'This is a puzzle game based on machine learning and SDGs14. We hope that students and children can truly understand AI from the perspective of machine learning, while also recognizing the harm of marine litter to the environment.',
    learnMore: 'Learn More',
    viewSource: 'View Source Code',
    
    // About Section
    about: 'About',
    aboutDescription: 'This is a puzzle game based on machine learning and SDGs14. We hope that students and children can truly understand AI from the perspective of machine learning, while also recognizing the harm of marine litter to the environment.',
    
    // Contributor Section
    contributor: 'Contributor',
    contributorName: 'Wei-Jun Chen',
    contributorEducation: 'Education: National Chengchi University, B.B.S. in Statistics',
    
    // Technical Skills Section
    technicalSkills: 'Technical Skills',
    frontend: 'Frontend',
    backend: 'Backend',
    aiRelated: 'AI Related',
    tools: 'Tools',
    
    // Contact Section
    contact: 'Contact Us',
    contactInformation: 'Contact Information',
    email: 'Email',
    homepage: 'homepage',
    location: 'Location',
    locationValue: 'Taipei, Taiwan',
    
    // Navigation
    navHome: 'Home',
    navEnvironment: 'Environment Setup',
    navManual: 'Manual Control',
    navCollect: 'Collect Data',
    navTrain: 'Train Model',
    navKNN: 'Use KNN Model',
    navTemplate: 'Custom Template',
    navSpeed: 'Speed Up',
    navContact: 'Contact',
    
    // Sections
    sectionEnvironment: 'Environment Setup',
    gitInstallTitle: '1️⃣ Install Git',
    gitInstallDesc: 'Download and install from the official website (just click Next):',
    gitInstallLink: 'https://git-scm.com/',
    gitInstallCheck: 'After installation, open terminal and type:',
    gitInstallCommand: 'git --version',
    gitInstallSuccess: 'If you see a version number, installation is successful.',
    gitCloneTitle: '2️⃣ Find the GitHub Project',
    gitCloneExample: 'For example, this game project:',
    gitCloneSteps: 'Click Code → HTTPS → Copy the link.',
    gitCloneFolderTitle: '3️⃣ Open a Folder for Projects',
    gitCloneFolderExample: 'For example:',
    gitCloneFolderPath: 'C:\\Users\\YourName\\Projects',
    gitCloneFolderAction: 'Right-click in this folder → Open in Terminal.',
    gitCloneCommandTitle: '4️⃣ Execute git clone',
    gitCloneCommandDesc: 'Paste the following command in terminal:',
    gitCloneCommand: 'git clone <the URL you just copied>',
    gitCloneCommandExample: 'For example:',
    gitCloneResult: 'After execution, you will see in the folder:',
    sectionManual: 'Manual Control',
    manualDesc: 'Execute in project directory:',
    manualCommand: 'python -m mlgame -i ./ml/ml_play_manual.py ./ --level 1',
    sectionCollect: 'Collect Movement Data',
    collectDesc: 'Execute in project directory:',
    collectCommand: 'python -m mlgame -i ./ml/ml_play_collect_data.py ./ --level 1',
    sectionTrain: 'Train KNN Model',
    trainDesc: 'Execute in project directory:',
    trainCommand: 'python ./ml/knn_train.py',
    sectionKNN: 'Use KNN Model',
    knnDesc: 'Execute in project directory:',
    knnCommand: 'python -m mlgame -i ./ml/ml_play_knn.py ./ --level 1',
    sectionTemplate: 'Custom Template',
    templateDesc: 'Execute in project directory:',
    templateCommand: 'python -m mlgame -i ./ml/ml_play_template.py ./ --level 1',
    sectionSpeed: 'Speed Up Game',
    speedDesc: 'Execute in project directory:',
    speedCommand: 'python -m mlgame -f 120 -i ./ml/ml_play_knn.py ./ --level 1',
    speedNote: '-f sets the fps parameter. The larger the value, the higher the fps.',
    
    // Footer
    footer: '© 2025 Wei-Jun Chen · Built with Next.js & shadcn/ui',
  },
}

export type Language = 'zh-TW' | 'zh-CN' | 'en'

