!function(e){var t={};function n(r){if(t[r])return t[r].exports;var o=t[r]={i:r,l:!1,exports:{}};return e[r].call(o.exports,o,o.exports,n),o.l=!0,o.exports}n.m=e,n.c=t,n.d=function(e,t,r){n.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},n.r=function(e){"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},n.t=function(e,t){if(1&t&&(e=n(e)),8&t)return e;if(4&t&&"object"==typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(n.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var o in e)n.d(r,o,function(t){return e[t]}.bind(null,o));return r},n.n=function(e){var t=e&&e.__esModule?function(){return e.default}:function(){return e};return n.d(t,"a",t),t},n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},n.p="",n(n.s=0)}([function(e,t){function n(e){var t=new Date(e),n=t.getDate(),r=t.getMonth();return t.getFullYear()+"年"+(r+1)+"月"+n+"日"}var r,o,a=new XMLHttpRequest;a.addEventListener("load",(r="latest-news-container",o="spotlight",function(e){var t,a,c,i,d,l,u,s,p=document.getElementById(r),f=p.querySelector("div.row"),m=JSON.parse(e.target.responseText);try{if(t=m.latest_articles){var h=function(e){for(var t=document.createDocumentFragment(),r=0;r<e.length;r++){var o=e[r],a='<a href="/blog/'.concat(o.slug,'">').concat(o.title.rendered,"</a>"),c="<h4>".concat(a,"</h4>"),i='<p class="u-no-padding--top">\n        <em>\n          <time pubdate datetime="'.concat(o.date,'">\n            ').concat(n(o.date),"\n          </time>\n        </em>\n      </p>"),d=document.createElement("div");d.classList.add("col-3"),d.innerHTML=" \n        ".concat(c,"\n        ").concat(i,"\n      "),t.appendChild(d)}return t}(t);f.appendChild(h);var g=document.createElement("h3");g.innerHTML="最新博客文章",p.insertBefore(g,f)}}catch(e){console.error("Error ".concat(e," occured when fetching the latest article data from the API"))}try{var v=m.latest_pinned_articles[0][0];if(v){p.classList.add("p-divider","col-9");var b=document.getElementById(o);b.classList.add("col-3","p-divider__block");var y=(a=v,c=document.createDocumentFragment(),i='<a href="/blog/'.concat(a.slug,'">').concat(a.title.rendered,"</a>"),d="<h4>".concat(i,"</h4>"),l='<p class="u-no-padding--top">\n      <em>\n        <time pubdate datetime="'.concat(a.date,'">\n            ').concat(n(a.date),"\n        </time>\n      </em>\n    </p>"),u="\n      ".concat(d,"\n      ").concat(l,"\n    "),(s=document.createElement("div")).innerHTML="\n    ".concat("<h3>Spotlight</h3>","\n    ").concat(u,"\n  "),c.appendChild(s),c);b.appendChild(y)}}catch(e){console.error('Error "'.concat(e,'" occured when trying to fetch the latest spotlight article from the API'))}})),a.open("GET","blog/latest-news"),a.send()}]);
