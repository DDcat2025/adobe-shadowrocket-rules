# Adobe AI, Behance & Stock Routing Rules

这个仓库把 Adobe 规则拆成代理和直连两类，避免把 Adobe 登录、Creative Cloud、
字体、证书、更新和常规桌面端服务全部放进代理。

## 规则范围

- `AdobeAI`：Adobe 软件和网页中生成式 AI / 智能生成相关端点，例如 Firefly、
  Photoshop Web、Illustrator Web、Sensei、Firefly 视频/音效、Captivate AI voices。
- `Behance`：Behance 网站和相关图片资源。
- `AdobeStock`：Adobe Stock 网站、投稿子站、Stock API、素材 CDN、Fotolia 旧站和专用素材下载端点。
- `AdobeDirect`：Adobe 登录、Creative Cloud、字体、更新、证书、常规网页和桌面端基础服务。

代理列表不包含以下通用服务：

- Adobe 登录：`adobelogin.com`、`account.adobe.com`
- Creative Cloud 常规服务：`creativecloud.com`、`adobecc.com`、`adobeccstatic.com`
- 字体服务：`typekit.com`、`typekit.net`、`fonts.adobe.com`
- 证书、统计、营销、Marketo、Magento 等 Adobe 旗下非目标业务

## Shadowrocket

把下面规则放在 `GEOIP` 和 `FINAL` 前，并把 `PROXY` 替换成你的代理策略组名称：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeAI/AdobeAI.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/Behance/Behance.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeStock/AdobeStock.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeDirect/AdobeDirect.list,DIRECT
```

如果你想用一份合并规则：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeProxy/AdobeProxy.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeDirect/AdobeDirect.list,DIRECT
```

代理规则必须放在 `AdobeDirect` 前面。要么使用 `AdobeAI` + `Behance` + `AdobeStock` 分开控制，
要么只使用 `AdobeProxy` 合并版，不要重复引用代理规则。

## 已有配置升级（2026-09-11）

使用 `AdobeProxy` 合并列表：刷新远程规则即可获得 Stock 代理规则。
使用 `AdobeAI` + `Behance` 分开列表：增加上面的 `AdobeStock` 引用，并放在 `AdobeDirect` 前面。
同时刷新直连列表，以移除旧的 Stock / ftcdn 显式直连条目。

`stock.adobe.com` 采用后缀规则，也覆盖 `contributor.stock.adobe.com`。
`ftcdn.net` 和 `astockcdn.net` 覆盖素材预览、音视频及静态资源子域名。
Stock API、落地页服务及官方列出的专用素材 S3 端点也走代理。
保留通用 `adobe.com` / `adobe.io` 直连兜底，依靠代理规则优先匹配；不要把直连列表放在前面。
范围是已核实的素材业务专用域名；共享登录、字体、统计和整个 AWS/CDN 域名不纳入 Stock 列表。
未来或临时新增端点仍需结合连接日志补充。

## Mihomo / Clash Meta

```yaml
rule-providers:
  adobe-ai:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Mihomo/AdobeAI/AdobeAI.yaml
    path: ./ruleset/adobe-ai.yaml
    interval: 86400
  behance:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Mihomo/Behance/Behance.yaml
    path: ./ruleset/behance.yaml
    interval: 86400
  adobe-stock:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Mihomo/AdobeStock/AdobeStock.yaml
    path: ./ruleset/adobe-stock.yaml
    interval: 86400
  adobe-direct:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Mihomo/AdobeDirect/AdobeDirect.yaml
    path: ./ruleset/adobe-direct.yaml
    interval: 86400

rules:
  - RULE-SET,adobe-ai,PROXY
  - RULE-SET,behance,PROXY
  - RULE-SET,adobe-stock,PROXY
  - RULE-SET,adobe-direct,DIRECT
```

## 文件

- `rule/Shadowrocket/AdobeAI/AdobeAI.list`：Adobe AI / 智能生成相关规则。
- `rule/Shadowrocket/Behance/Behance.list`：Behance 规则。
- `rule/Shadowrocket/AdobeStock/AdobeStock.list`：Adobe Stock 素材站与专用资源规则。
- `rule/Shadowrocket/AdobeProxy/AdobeProxy.list`：AdobeAI + Behance + AdobeStock 合并规则。
- `rule/Shadowrocket/AdobeDirect/AdobeDirect.list`：Adobe 常规直连规则。
- `rule/Mihomo/*/*.yaml`：Mihomo classical rule-provider 格式。
- `data/*.txt`：维护用域名清单。

## 参考

- [Adobe 官方网络端点文档](https://helpx.adobe.com/business/enterprise/manage-services/configure-services/network-endpoints.html)。
- [Adobe Stock API 文档](https://developer.adobe.com/stock/docs/api/)。
- Adobe Captivate 受限网络功能端点说明。
- blackmatrix7 的 Adobe Shadowrocket 总规则。

本仓库刻意不复刻全量 Adobe 列表，而是只拆出需要代理的目标业务。
