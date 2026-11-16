"use strict";

// 第一步：后端以后需要提供这个接口，返回新闻数组。
// 当前 display_data.py 还没有 /api/news，所以初始页面不自动请求它。
// 后端返回格式：[{ time 或 pubDate, title, content, summary, analysis }]
// 前端不会读取电脑磁盘路径，也不会把 data/news.json 复制到 static。
const API_URL = "/api/news";

// 第二步：找到 HTML 中要使用的元素。
const newsList = document.getElementById("news-list");
const newsTemplate = document.getElementById("news-template");
const searchInput = document.getElementById("search-input");
const loadButton = document.getElementById("load-button");
const statusText = document.getElementById("status");
const countText = document.getElementById("news-count");
const latestTimeText = document.getElementById("latest-time");

// 只在当前页面的内存中保存后端返回的数据。
let allNews = [];
let hasLoaded = false;

// 兼容实际数据的 pubDate 字段，以及以后可能使用的 time 字段。
function getNewsTime(news) {
  return news.time || news.pubDate || "";
}

// 第三步：复制 HTML 模板，把一条新闻填入页面。
function createNewsCard(news) {
  const card = newsTemplate.content.cloneNode(true);

  // 使用 textContent 显示纯文本，新闻里的 HTML 不会被当成代码执行。
  card.querySelector(".news-time").textContent =
    "发布时间：" + (getNewsTime(news) || "未提供");
  card.querySelector(".news-title").textContent = news.title || "无标题";
  card.querySelector(".news-content").textContent =
    news.content || "暂无原文";
  card.querySelector(".news-summary").textContent =
    news.summary || "暂无 AI 概括";
  card.querySelector(".news-analysis").textContent =
    news.analysis || "暂无 AI 分析";

  return card;
}

// 第四步：按标题搜索，然后显示新闻。不改动原始数组。
function renderNews() {
  const keyword = searchInput.value.trim().toLowerCase();
  const visibleNews = allNews.filter(function (news) {
    return String(news.title || "").toLowerCase().includes(keyword);
  });

  newsList.replaceChildren();
  const fragment = document.createDocumentFragment();

  for (const news of visibleNews) {
    fragment.appendChild(createNewsCard(news));
  }

  newsList.appendChild(fragment);
  if (hasLoaded) {
    statusText.textContent =
      "显示 " + visibleNews.length + " 条，共 " + allNews.length + " 条新闻。";
  }
}

function updateOverview() {
  countText.textContent = allNews.length;
  let latestTime = "";
  let latestValue = -Infinity;

  for (const news of allNews) {
    const time = getNewsTime(news);
    const value = Date.parse(time);
    if (!Number.isNaN(value) && value > latestValue) {
      latestValue = value;
      latestTime = time;
    }
  }

  // 原始时间没有时区时，保持原样显示，不擅自转为北京时间或 UTC。
  latestTimeText.textContent = latestTime || "暂无有效时间";
}

// 第五步：通过 HTTP 请求 FastAPI；成功后才替换当前新闻数据。
async function loadNews() {
  loadButton.disabled = true;
  statusText.textContent = "正在从后端加载新闻…";

  try {
    const response = await fetch(API_URL, { cache: "no-store" });
    if (response.status === 404) {
      throw new Error("FastAPI 尚未提供 /api/news 接口，需要先在后端添加路由。");
    }
    if (!response.ok) {
      throw new Error("请求失败，HTTP 状态码：" + response.status);
    }

    const data = await response.json();
    if (!Array.isArray(data)) {
      throw new Error("接口应该返回一个新闻数组。");
    }
    if (data.some((news) => !news || typeof news !== "object" || Array.isArray(news))) {
      throw new Error("数组中的每条新闻都应该是一个对象。");
    }

    allNews = data;
    hasLoaded = true;
    updateOverview();
    renderNews();
  } catch (error) {
    statusText.textContent = "加载失败：" + error.message;
    // 请求失败时不清空已有新闻，便于排查接口问题。
  } finally {
    loadButton.disabled = false;
  }
}

// 第六步：绑定按钮和搜索事件。页面初始没有内置新闻。
loadButton.addEventListener("click", loadNews);
searchInput.addEventListener("input", renderNews);

// 后端接口做好后，如需进入页面就加载，取消下一行的注释即可。
// loadNews();
