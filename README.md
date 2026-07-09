# Adobe AI & Behance Shadowrocket Rules

这个仓库把 Adobe 规则拆成代理和直连两类，避免把 Adobe 登录、Creative Cloud、
字体、证书、更新和常规桌面端服务全部放进代理。

## 规则范围

- `AdobeAI`：Adobe 软件和网页中生成式 AI / 智能生成相关端点，例如 Firefly、
  Photoshop Web、Illustrator Web、Sensei、Firefly 视频/音效、Captivate AI voices。
- `Behance`：Behance 网站和相关图片资源。
- `AdobeDirect`：Adobe 登录、Creative Cloud、字体、更新、证书、常规网页和桌面端基础服务。

`AdobeAI` 和 `Behance` 不包含：

- Adobe 登录：`adobelogin.com`、`account.adobe.com`
- Creative Cloud 常规服务：`creativecloud.com`、`adobecc.com`、`adobeccstatic.com`
- 字体服务：`typekit.com`、`typekit.net`、`fonts.adobe.com`
- 证书、统计、营销、Marketo、Magento、Fotolia 等 Adobe 旗下非目标业务

## Shadowrocket

把下面两行放在 `GEOIP` 和 `FINAL` 前，并把 `PROXY` 替换成你的代理策略组名称：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeAI/AdobeAI.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/Behance/Behance.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeDirect/AdobeDirect.list,DIRECT
```

如果你想用一份合并规则：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeProxy/AdobeProxy.list,PROXY
RULE-SET,https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Shadowrocket/AdobeDirect/AdobeDirect.list,DIRECT
```

代理规则必须放在 `AdobeDirect` 前面。要么使用 `AdobeAI` + `Behance` 分开控制，
要么只使用 `AdobeProxy` 合并版，不要重复引用代理规则。

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
  adobe-direct:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/adobe-shadowrocket-rules/main/rule/Mihomo/AdobeDirect/AdobeDirect.yaml
    path: ./ruleset/adobe-direct.yaml
    interval: 86400

rules:
  - RULE-SET,adobe-ai,PROXY
  - RULE-SET,behance,PROXY
  - RULE-SET,adobe-direct,DIRECT
```

## 文件

- `rule/Shadowrocket/AdobeAI/AdobeAI.list`：Adobe AI / 智能生成相关规则。
- `rule/Shadowrocket/Behance/Behance.list`：Behance 规则。
- `rule/Shadowrocket/AdobeProxy/AdobeProxy.list`：AdobeAI + Behance 合并规则。
- `rule/Shadowrocket/AdobeDirect/AdobeDirect.list`：Adobe 常规直连规则。
- `rule/Mihomo/*/*.yaml`：Mihomo classical rule-provider 格式。
- `data/*.txt`：维护用域名清单。

## 参考

- Adobe 官方网络端点文档。
- Adobe Captivate 受限网络功能端点说明。
- blackmatrix7 的 Adobe Shadowrocket 总规则。

本仓库刻意不复刻全量 Adobe 列表，而是只拆出需要代理的目标业务。
