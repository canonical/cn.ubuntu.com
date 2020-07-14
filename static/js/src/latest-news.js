function formatDate(date) {
  const parsedDate = new Date(date);

  const day = parsedDate.getDate();
  const monthIndex = parsedDate.getMonth();
  const year = parsedDate.getFullYear();

  return year + '年' + (monthIndex + 1) + '月' + day + '日';
}

function htmlForLatestArticles(articles) {
  const articlesTree = document.createDocumentFragment();
  for (let i = 0; i < articles.length; i++) {
    const article = articles[i];
    const link = `<a href="/blog/${article.slug}">${article.title.rendered}</a>`;
    const header = `<h4>${link}</h4>`;
    const date = `<p class="u-no-padding--top">
        <em>
          <time pubdate datetime="${article.date}">
            ${formatDate(article.date)}
          </time>
        </em>
      </p>`;
    const div = document.createElement('div');
    div.classList.add('col-3');
    div.innerHTML = ` 
        ${header}
        ${date}
      `;

    articlesTree.appendChild(div);
  }
  return articlesTree;
}

function htmlForLatestPinnedArticle(article) {
  const articlesTree = document.createDocumentFragment();

  // "Featured"
  const header = '<h3>Spotlight</h3>';

  const link = `<a href="/blog/${article.slug}">${article.title.rendered}</a>`;
  const linkHeader = `<h4>${link}</h4>`;

  const date = `<p class="u-no-padding--top">
      <em>
        <time pubdate datetime="${article.date}">
            ${formatDate(article.date)}
        </time>
      </em>
    </p>`;

  const innerDiv = `
      ${linkHeader}
      ${date}
    `;

  const div = document.createElement('div');
  div.innerHTML = `
    ${header}
    ${innerDiv}
  `;

  articlesTree.appendChild(div);

  return articlesTree;
}

const createReqListenerForDomContainer = (
  latestNewsContainer,
  spotlightContainer
) => event => {
  const containerForLatestNews = document.getElementById(latestNewsContainer);

  const containerForLatestArticles = containerForLatestNews.querySelector(
    'div.row'
  );

  const data = JSON.parse(event.target.responseText);
  let latest;
  try {
    latest = data.latest_articles;
    if (latest) {
      const html = htmlForLatestArticles(latest);
      containerForLatestArticles.appendChild(html);

      const heading = document.createElement('h3');
      // "Latest news"
      heading.innerHTML = '最新博客文章';
      containerForLatestNews.insertBefore(heading, containerForLatestArticles);
    }
  } catch (error) {
    /* eslint-disable no-console */
    console.error(
      `Error ${error} occured when fetching the latest article data from the API`
    );
    /* eslint-enable no-console */
  }

  try {
    const latestPinned = data.latest_pinned_articles[0][0];
    if (latestPinned) {
      containerForLatestNews.classList.add('p-divider', 'col-9');

      const containerForSpotlight = document.getElementById(spotlightContainer);
      containerForSpotlight.classList.add('col-3', 'p-divider__block');

      const htmlSpotLight = htmlForLatestPinnedArticle(latestPinned);
      containerForSpotlight.appendChild(htmlSpotLight);
    }
  } catch (error) {
    /* eslint-disable no-console */
    console.error(
      `Error "${error}" occured when trying to fetch the latest spotlight article from the API`
    );
    /* eslint-enable no-console */
  }
};

const oReq = new XMLHttpRequest();
oReq.addEventListener(
  'load',
  createReqListenerForDomContainer('latest-news-container', 'spotlight')
);
oReq.open('GET', 'blog/latest-news');
oReq.send();
