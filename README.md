# -import { useState, useCallback } from "react";

const TODAY = new Date().toISOString().split("T")[0];
const TODAY_KR = new Date().toLocaleDateString("ko-KR", { year: "numeric", month: "long", day: "numeric" });

const CATS = [
  { id: "gov", label: "정부지원사업", emoji: "🏛️", bg: "#EFF6FF", border: "#BFDBFE", accent: "#1D4ED8", light: "#DBEAFE" },
  { id: "fund", label: "정책자금", emoji: "💰", bg: "#F0FDF4", border: "#BBF7D0", accent: "#15803D", light: "#DCFCE7" },
  { id: "cert", label: "기업인증", emoji: "🏆", bg: "#FFFBEB", border: "#FDE68A", accent: "#B45309", light: "#FEF3C7" },
  { id: "corp", label: "법인전환·기업설립", emoji: "🏢", bg: "#F5F3FF", border: "#DDD6FE", accent: "#6D28D9", light: "#EDE9FE" },
];

const SOURCES = [
  { name: "K-스타트업", icon: "🚀" },
  { name: "기업마당", icon: "🏢" },
  { name: "중소벤처기업부", icon: "🏛️" },
  { name: "중소기업진흥공단", icon: "💼" },
  { name: "기술보증기금", icon: "🛡️" },
  { name: "신용보증기금", icon: "✅" },
  { name: "지자체 진흥원", icon: "📍" },
];

const QUICK_KW = [
  { cat: "gov", examples: ["2025 창업지원사업 공고", "중소기업 R&D 지원사업", "소상공인 정부지원 최신공고"] },
  { cat: "fund", examples: ["중소기업 정책자금 융자", "기술보증기금 보증", "IBK 창업기업 대출"] },
  { cat: "cert", examples: ["벤처기업 인증 신청", "이노비즈 인증 2025", "메인비즈 인증 혜택"] },
  { cat: "corp", examples: ["법인전환 지원사업", "기업부설연구소 설립", "1인창조기업 지원"] },
];

const SEARCH_SYSTEM = `오늘 날짜는 ${TODAY_KR} (${TODAY})입니다.
당신은 대한민국 정부지원사업·정책자금 공고 검색 전문가입니다.
웹 검색 도구를 사용하여 아래 출처에서 최신 공고를 검색하세요:
1. K-스타트업 (k-startup.go.kr)
2. 기업마당 (bizinfo.go.kr)
3. 중소벤처기업부 (mss.go.kr)
4. 중소기업진흥공단 (kosmes.or.kr)
5. 기술보증기금·신용보증기금
6. 각 지자체 경제진흥원
7. 관련 최신 뉴스

필터링 규칙: 마감일이 ${TODAY} 이전인 공고는 반드시 제외. 최근 1개월 이내 공고 우선.

반드시 아래 순수 JSON만 반환 (마크다운 없이):
{
  "announcements": [
    {
      "title": "공고명",
      "source": "출처기관명",
      "sourceUrl": "URL",
      "deadline": "YYYY-MM-DD 또는 상시 또는 미정",
      "budget": "지원규모 또는 null",
      "target": "지원대상",
      "summary": "핵심내용 2-3줄",
      "category": "gov/fund/cert/corp 중 하나",
      "isRecent": true
    }
  ],
  "newsHighlight": "최신 뉴스 동향 1-2줄"
}`;

const BLOG_SYSTEM = `당신은 히어컴퍼니(HereCompany) 전문 블로그 작가입니다.
히어컴퍼니: 중소기업·스타트업 전문 컨설팅 (법인전환, 연구소 설립, 벤처/이노비즈 인증, 정부지원사업, 정책자금).
오늘 날짜: ${TODAY_KR}

작성 원칙:
- 실제 검색된 공고 정보 정확히 반영 (날짜·금액·기관명)
- 실용적이고 즉시 행동 가능한 정보
- 히어컴퍼니 전문성 자연스럽게 어필
- 마지막 CTA: 히어컴퍼니 무료상담 안내

순수 JSON만 반환:
{
  "title": "SEO 제목 (40-60자)",
  "metaDescription": "메타설명 (150-160자)",
  "content": "HTML 본문 (h2/h3/p/ul/li/strong, 약 2000자, CTA 포함)",
  "snsText": "SNS 공유문 (이모지, 200자 이내, [링크] 포함)",
  "tags": ["태그1","태그2","태그3","태그4","태그5"],
  "readTime": 6,
  "slug": "url-slug",
  "highlight": "핵심 인사이트 한 줄"
}`;

export default function App() {
  const [kw, setKw] = useState("");
  const [cat, setCat] = useState("gov");
  const [ctx, setCtx] = useState("");
  const [phase, setPhase] = useState("idle");
  const [announcements, setAnnouncements] = useState([]);
  const [newsHighlight, setNewsHighlight] = useState("");
  const [result, setResult] = useState(null);
  const [tab, setTab] = useState("content");
  const [copied, setCopied] = useState("");
  const [history, setHistory] = useState([]);
  const [errorMsg, setErrorMsg] = useState("");
  const [selectedAnns, setSelectedAnns] = useState([]);
  const [showQuick, setShowQuick] = useState(true);

  const selCat = CATS.find(c => c.id === cat);
  const isLoading = phase === "searching" || phase === "writing";

  const copy = (text, key) => {
    navigator.clipboard.writeText(text);
    setCopied(key);
    setTimeout(() => setCopied(""), 2000);
  };

  const searchAnnouncements = useCallback(async () => {
    if (!kw.trim()) return;
    setPhase("searching");
    setAnnouncements([]);
    setResult(null);
    setErrorMsg("");
    setShowQuick(false);
    const catLabel = CATS.find(c => c.id === cat)?.label;
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: SEARCH_SYSTEM,
          tools: [{ type: "web_search_20250305", name: "web_search" }],
          messages: [{ role: "user", content: `카테고리: ${catLabel}\n검색 키워드: ${kw}${ctx ? `\n추가 조건: ${ctx}` : ""}\n\n최신 유효 공고를 검색해주세요.` }],
        }),
      });
      const data = await res.json();
      const textBlock = data.content?.find(b => b.type === "text");
      if (!textBlock) throw new Error("검색 결과 없음");
      const jsonMatch = textBlock.text.replace(/```json|```/g, "").trim().match(/\{[\s\S]*\}/);
      if (!jsonMatch) throw new Error("데이터 파싱 실패");
      const parsed = JSON.parse(jsonMatch[0]);
      const valid = (parsed.announcements || []).filter(a => {
        if (!a.deadline || a.deadline === "상시" || a.deadline === "미정") return true;
        return a.deadline >= TODAY;
      });
      setAnnouncements(valid);
      setNewsHighlight(parsed.newsHighlight || "");
      setSelectedAnns(valid.map((_, i) => i));
      setPhase("found");
    } catch (e) {
      setErrorMsg("공고 검색 중 오류가 발생했습니다. 다시 시도해주세요.");
      setPhase("error");
    }
  }, [kw, cat, ctx]);

  const generateBlog = useCallback(async () => {
    setPhase("writing");
    const catLabel = CATS.find(c => c.id === cat)?.label;
    const selAnns = announcements.filter((_, i) => selectedAnns.includes(i));
    const userMsg = `카테고리: ${catLabel}\n키워드: ${kw}\n오늘: ${TODAY_KR}\n${ctx ? `맥락: ${ctx}\n` : ""}
【검색된 공고 목록】
${selAnns.map((a, i) => `[${i+1}] ${a.title} | ${a.source} | 마감: ${a.deadline} | 규모: ${a.budget || "별도확인"} | 대상: ${a.target}\n${a.summary}`).join("\n\n")}
${newsHighlight ? `\n【뉴스 동향】\n${newsHighlight}` : ""}`;
    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: BLOG_SYSTEM,
          messages: [{ role: "user", content: userMsg }],
        }),
      });
      const data = await res.json();
      const text = data.content?.find(b => b.type === "text")?.text || "";
      const jsonMatch = text.replace(/```json|```/g, "").trim().match(/\{[\s\S]*\}/);
      if (!jsonMatch) throw new Error("블로그 파싱 실패");
      const parsed = JSON.parse(jsonMatch[0]);
      setResult(parsed);
      setHistory(h => [{ kw, cat, catLabel, r: parsed, cnt: selAnns.length }, ...h.slice(0, 7)]);
      setTab("content");
      setPhase("done");
    } catch (e) {
      setErrorMsg("블로그 생성 중 오류가 발생했습니다.");
      setPhase("error");
    }
  }, [kw, cat, ctx, announcements, selectedAnns, newsHighlight]);

  const wpCode = (r) => `<!-- wp:heading {"level":1} -->
<h1 class="wp-block-heading">${r.title}</h1>
<!-- /wp:heading -->
<!-- wp:paragraph -->
<p><em>${TODAY_KR} 기준 최신 공고 | 읽기: 약 ${r.readTime}분</em></p>
<!-- /wp:paragraph -->
<!-- wp:html -->
${r.content}
<!-- /wp:html -->
<!--
[SEO 설정 - Yoast SEO / Rank Math]
제목: ${r.title}
메타설명: ${r.metaDescription}
슬러그: ${r.slug}
태그: ${r.tags?.join(", ")}
-->`;

  return (
    <div style={{ fontFamily: "'Apple SD Gothic Neo','Malgun Gothic',sans-serif", minHeight: "100vh", background: "#0D1117", color: "#E2E8F0" }}>
      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeIn { from { opacity:0; transform:translateY(6px); } to { opacity:1; transform:translateY(0); } }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.45} }
        .ann-card { transition: border-color 0.15s, transform 0.12s; }
        .ann-card:hover { border-color: #C8A96E !important; transform: translateY(-1px); }
        .kwbtn { transition: all 0.15s; }
        .kwbtn:hover { transform: translateY(-1px); }
        .tabBtn { transition: color 0.12s; }
        .tabBtn:hover { color: #E8C97E !important; }
        .cpBtn { transition: opacity 0.12s; }
        .cpBtn:hover { opacity: 0.82; }
      `}</style>

      {/* Header */}
      <div style={{ background: "#161B22", borderBottom: "1px solid #30363D", padding: "13px 20px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 11 }}>
          <div style={{ width: 36, height: 36, background: "linear-gradient(135deg,#C8A96E,#F0D080)", borderRadius: 9, display: "flex", alignItems: "center", justifyContent: "center", fontWeight: 900, fontSize: 19, color: "#0D1117" }}>H</div>
          <div>
            <div style={{ color: "#E8C97E", fontWeight: 900, fontSize: 14, letterSpacing: "0.06em" }}>HERECOMPANY 블로그 자동화</div>
            <div style={{ color: "#6E7681", fontSize: 11 }}>실시간 공고 검색 · AI 블로그 생성 · 워드프레스 연동</div>
          </div>
        </div>
        <div style={{ textAlign: "right", fontSize: 11 }}>
          <div style={{ color: "#3FB950", fontWeight: 700 }}>● LIVE</div>
          <div style={{ color: "#6E7681" }}>{TODAY_KR}</div>
        </div>
      </div>

      {/* Source bar */}
      <div style={{ background: "#161B22", borderBottom: "1px solid #21262D", padding: "7px 20px", display: "flex", gap: 7, flexWrap: "wrap", alignItems: "center" }}>
        <span style={{ fontSize: 10, color: "#6E7681", fontWeight: 700, letterSpacing: "0.08em" }}>검색 출처</span>
        {SOURCES.map(s => (
          <span key={s.name} style={{ fontSize: 10, padding: "2px 7px", borderRadius: 4, background: "#21262D", color: "#8B949E", border: "1px solid #30363D", fontWeight: 600 }}>{s.icon} {s.name}</span>
        ))}
      </div>

      <div style={{ maxWidth: 900, margin: "0 auto", padding: "18px 14px", display: "grid", gap: 14 }}>

        {/* ── INPUT CARD ── */}
        <div style={{ background: "#161B22", borderRadius: 13, padding: "20px 22px", border: "1px solid #30363D", animation: "fadeIn 0.3s ease" }}>
          <div style={{ fontSize: 10, fontWeight: 700, color: "#8B949E", letterSpacing: "0.12em", marginBottom: 10 }}>STEP 1 · 카테고리</div>
          <div style={{ display: "flex", gap: 7, flexWrap: "wrap", marginBottom: 18 }}>
            {CATS.map(c => (
              <button key={c.id} onClick={() => setCat(c.id)} style={{
                padding: "7px 13px", borderRadius: 20, border: `2px solid ${cat === c.id ? c.accent : "#30363D"}`,
                background: cat === c.id ? c.bg : "#21262D", color: cat === c.id ? c.accent : "#8B949E",
                fontWeight: cat === c.id ? 700 : 500, fontSize: 12, cursor: "pointer", transition: "all 0.15s"
              }}>{c.emoji} {c.label}</button>
            ))}
          </div>

          <div style={{ fontSize: 10, fontWeight: 700, color: "#8B949E", letterSpacing: "0.12em", marginBottom: 7 }}>STEP 2 · 검색 키워드 입력</div>
          <div style={{ display: "flex", gap: 8, marginBottom: 9 }}>
            <input value={kw} onChange={e => setKw(e.target.value)} onKeyDown={e => e.key === "Enter" && !isLoading && searchAnnouncements()}
              placeholder="예: 2025 중소기업 정책자금, 벤처기업 인증, 창업지원사업..."
              style={{ flex: 1, padding: "10px 13px", borderRadius: 8, border: "1.5px solid #30363D", fontSize: 13, outline: "none", background: "#0D1117", color: "#E2E8F0" }} />
            <button onClick={searchAnnouncements} disabled={isLoading || !kw.trim()} style={{
              padding: "10px 18px", background: isLoading ? "#21262D" : "linear-gradient(135deg,#C8A96E,#E8A020)",
              color: isLoading ? "#6E7681" : "#0D1117", borderRadius: 8, border: "none",
              fontWeight: 700, fontSize: 13, cursor: isLoading ? "not-allowed" : "pointer", minWidth: 110, transition: "all 0.15s"
            }}>{phase === "searching" ? "🔍 검색중..." : phase === "writing" ? "✍️ 작성중..." : "🔍 공고 검색"}</button>
          </div>
          <textarea value={ctx} onChange={e => setCtx(e.target.value)} rows={2}
            placeholder="추가 조건 (선택): 특정 지역·업종·금액대·기업규모 등"
            style={{ width: "100%", padding: "9px 13px", borderRadius: 8, border: "1.5px solid #30363D", fontSize: 12, color: "#8B949E", resize: "vertical", boxSizing: "border-box", background: "#0D1117" }} />

          {/* ── QUICK KEYWORDS - 항상 표시 ── */}
          <div style={{ marginTop: 16, borderTop: "1px solid #21262D", paddingTop: 14 }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
              <span style={{ fontSize: 10, fontWeight: 700, color: "#8B949E", letterSpacing: "0.12em" }}>⚡ 빠른 검색 예시 — 클릭하면 바로 입력됩니다</span>
              <button onClick={() => setShowQuick(v => !v)} style={{ background: "none", border: "none", color: "#6E7681", cursor: "pointer", fontSize: 11 }}>{showQuick ? "접기 ▲" : "펼치기 ▼"}</button>
            </div>
            {showQuick && (
              <div style={{ display: "grid", gap: 9 }}>
                {QUICK_KW.map(group => {
                  const c = CATS.find(x => x.id === group.cat);
                  return (
                    <div key={group.cat} style={{ display: "flex", gap: 6, alignItems: "center", flexWrap: "wrap" }}>
                      <span style={{ fontSize: 11, fontWeight: 700, color: c?.accent, minWidth: 90, flexShrink: 0 }}>{c?.emoji} {c?.label}</span>
                      {group.examples.map(ex => (
                        <button key={ex} className="kwbtn" onClick={() => { setCat(group.cat); setKw(ex); }}
                          style={{ padding: "5px 10px", background: "#0D1117", border: `1.5px solid ${c?.border}`, borderRadius: 6, fontSize: 12, color: c?.accent, cursor: "pointer", fontWeight: 500 }}>{ex}</button>
                      ))}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* ── LOADING ── */}
        {isLoading && (
          <div style={{ background: "#161B22", borderRadius: 13, padding: 18, border: "1px solid #30363D", animation: "fadeIn 0.3s ease" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
              <div style={{ width: 18, height: 18, border: "2px solid #C8A96E", borderTopColor: "transparent", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} />
              <span style={{ fontWeight: 700, color: "#C8A96E", fontSize: 14 }}>{phase === "searching" ? "공고 실시간 검색 중..." : "AI 블로그 작성 중..."}</span>
            </div>
            {(phase === "searching" ? ["K-스타트업 공고 검색","기업마당 공고 검색","중소벤처기업부·지자체 공고 검색","마감일 필터링 (만료 공고 제외)"]
              : ["공고 검색 완료 ✅","SEO 제목·메타설명 생성","전문 블로그 본문 작성","SNS 요약·워드프레스 코드 생성"]
            ).map((txt, i) => (
              <div key={i} style={{ display: "flex", gap: 8, alignItems: "center", fontSize: 12, color: phase === "writing" && i === 0 ? "#3FB950" : "#6E7681", marginBottom: 5, animation: phase === "searching" ? `pulse ${1.2 + i * 0.25}s ease infinite` : "none" }}>
                <span>{phase === "writing" && i === 0 ? "✅" : "⏳"}</span>{txt}
              </div>
            ))}
          </div>
        )}

        {/* ── ERROR ── */}
        {phase === "error" && (
          <div style={{ background: "#1C1010", borderRadius: 13, padding: "14px 18px", border: "1px solid #6E2020", color: "#F85149", fontSize: 13, display: "flex", alignItems: "center", gap: 10 }}>
            ⚠️ {errorMsg}
            <button onClick={() => { setPhase("idle"); setShowQuick(true); }} style={{ marginLeft: "auto", padding: "5px 12px", background: "#21262D", border: "none", borderRadius: 7, color: "#E2E8F0", cursor: "pointer", fontSize: 12 }}>↩ 다시 시도</button>
          </div>
        )}

        {/* ── ANNOUNCEMENTS ── */}
        {(phase === "found" || phase === "done" || phase === "writing") && announcements.length > 0 && (
          <div style={{ background: "#161B22", borderRadius: 13, padding: "18px 22px", border: "1px solid #30363D", animation: "fadeIn 0.3s ease" }}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: newsHighlight ? 8 : 12, flexWrap: "wrap", gap: 8 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 12, fontWeight: 700, color: "#3FB950" }}>✅ 유효 공고 {announcements.length}건</span>
                <span style={{ fontSize: 11, color: "#6E7681" }}>({TODAY_KR} 기준 마감 미도래)</span>
              </div>
              {phase === "found" && (
                <button onClick={generateBlog} disabled={selectedAnns.length === 0} style={{ padding: "8px 18px", background: "linear-gradient(135deg,#1D4ED8,#2563EB)", color: "#FFF", borderRadius: 8, border: "none", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>✍️ 블로그 생성 →</button>
              )}
            </div>
            {newsHighlight && (
              <div style={{ padding: "8px 12px", background: "#0D1117", borderRadius: 8, fontSize: 12, color: "#8B949E", marginBottom: 12, borderLeft: "3px solid #C8A96E" }}>📰 최신 동향: {newsHighlight}</div>
            )}
            <div style={{ display: "grid", gap: 7 }}>
              {announcements.map((a, i) => {
                const c = CATS.find(x => x.id === a.category) || selCat;
                const isSel = selectedAnns.includes(i);
                const isExpiring = a.deadline && a.deadline !== "상시" && a.deadline !== "미정" && new Date(a.deadline) - new Date() < 7 * 86400000;
                return (
                  <div key={i} className="ann-card" onClick={() => setSelectedAnns(s => s.includes(i) ? s.filter(x => x !== i) : [...s, i])}
                    style={{ padding: "11px 13px", border: `1.5px solid ${isSel ? c.accent : "#30363D"}`, borderRadius: 9, background: "#0D1117", cursor: "pointer" }}>
                    <div style={{ display: "flex", gap: 9 }}>
                      <div style={{ width: 17, height: 17, borderRadius: 4, border: `2px solid ${isSel ? c.accent : "#30363D"}`, background: isSel ? c.accent : "none", flexShrink: 0, marginTop: 2, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 10, color: "#FFF" }}>{isSel ? "✓" : ""}</div>
                      <div style={{ flex: 1 }}>
                        <div style={{ display: "flex", gap: 5, flexWrap: "wrap", marginBottom: 4, alignItems: "center" }}>
                          <span style={{ fontSize: 11, fontWeight: 700, padding: "2px 7px", background: c.bg, color: c.accent, borderRadius: 7 }}>{c.emoji} {a.source}</span>
                          {isExpiring && <span style={{ fontSize: 10, fontWeight: 700, color: "#F85149", background: "#1C1010", padding: "1px 6px", borderRadius: 5 }}>⚡ 마감임박</span>}
                          {a.deadline === "상시" && <span style={{ fontSize: 10, color: "#3FB950", background: "#0D2A1C", padding: "1px 6px", borderRadius: 5 }}>♾️ 상시</span>}
                          {a.deadline && a.deadline !== "상시" && a.deadline !== "미정" && !isExpiring && <span style={{ fontSize: 10, color: "#8B949E" }}>📅 ~{a.deadline}</span>}
                          {a.budget && <span style={{ fontSize: 10, color: "#C8A96E", fontWeight: 700 }}>💰 {a.budget}</span>}
                        </div>
                        <div style={{ fontSize: 13, fontWeight: 700, color: "#E2E8F0", marginBottom: 3, lineHeight: 1.4 }}>{a.title}</div>
                        <div style={{ fontSize: 12, color: "#8B949E", lineHeight: 1.6 }}>{a.summary}</div>
                        {a.target && <div style={{ fontSize: 11, color: "#6E7681", marginTop: 3 }}>👥 {a.target}</div>}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
            {phase === "found" && (
              <div style={{ marginTop: 11, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontSize: 12, color: "#6E7681" }}>{selectedAnns.length}개 선택 (클릭으로 선택/해제)</span>
                <button onClick={generateBlog} disabled={selectedAnns.length === 0} style={{
                  padding: "9px 22px", background: selectedAnns.length === 0 ? "#21262D" : "linear-gradient(135deg,#C8A96E,#E8A020)",
                  color: selectedAnns.length === 0 ? "#6E7681" : "#0D1117", borderRadius: 8, border: "none", fontWeight: 700, fontSize: 13, cursor: selectedAnns.length === 0 ? "not-allowed" : "pointer"
                }}>✨ {selectedAnns.length}건 공고로 블로그 생성</button>
              </div>
            )}
          </div>
        )}

        {/* ── BLOG RESULT ── */}
        {result && phase === "done" && (
          <div style={{ background: "#161B22", borderRadius: 13, padding: "20px 22px", border: "1px solid #30363D", animation: "fadeIn 0.3s ease" }}>
            <div style={{ padding: "13px 15px", background: "#0D1117", borderRadius: 9, marginBottom: 14, borderLeft: `4px solid ${selCat?.accent}` }}>
              <div style={{ fontSize: 10, fontWeight: 700, color: selCat?.accent, marginBottom: 4, letterSpacing: "0.08em" }}>{selCat?.emoji} {selCat?.label} · {TODAY_KR} · 약 {result.readTime}분</div>
              <div style={{ fontSize: 16, fontWeight: 900, color: "#E2E8F0", lineHeight: 1.45, marginBottom: result.highlight ? 6 : 8 }}>{result.title}</div>
              {result.highlight && <div style={{ fontSize: 12, color: "#C8A96E", fontStyle: "italic", marginBottom: 8 }}>💡 {result.highlight}</div>}
              <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
                {result.tags?.map(t => <span key={t} style={{ padding: "2px 8px", background: "#21262D", borderRadius: 9, fontSize: 10, color: selCat?.accent, border: `1px solid ${selCat?.border}` }}>#{t}</span>)}
              </div>
            </div>

            {/* Tabs */}
            <div style={{ display: "flex", gap: 2, borderBottom: "1px solid #21262D", marginBottom: 14 }}>
              {[["content","📄 본문"],["seo","🔍 SEO"],["sns","📲 SNS"],["wp","⬆️ 워드프레스"]].map(([id,lbl]) => (
                <button key={id} className="tabBtn" onClick={() => setTab(id)} style={{
                  padding: "7px 13px", border: "none", background: "none", cursor: "pointer", fontSize: 12,
                  fontWeight: tab === id ? 700 : 400, color: tab === id ? "#E8C97E" : "#6E7681",
                  borderBottom: tab === id ? "2px solid #C8A96E" : "2px solid transparent", marginBottom: -1
                }}>{lbl}</button>
              ))}
            </div>

            {tab === "content" && (
              <div>
                <div style={{ background: "#0D1117", borderRadius: 9, padding: "16px 18px", fontSize: 13, lineHeight: 1.9, color: "#C9D1D9", border: "1px solid #21262D" }} dangerouslySetInnerHTML={{ __html: result.content }} />
                <button className="cpBtn" onClick={() => copy(result.content, "c")} style={{ marginTop: 10, padding: "7px 15px", background: copied==="c"?"#238636":"#21262D", color: copied==="c"?"#FFF":"#C8A96E", borderRadius: 7, border: `1px solid ${copied==="c"?"#238636":"#30363D"}`, fontSize: 12, fontWeight: 700, cursor: "pointer" }}>{copied==="c"?"✅ 복사됨!":"📋 HTML 본문 복사"}</button>
              </div>
            )}

            {tab === "seo" && (
              <div style={{ display: "grid", gap: 10 }}>
                {[
                  { lbl: `🏷️ SEO 제목 (${result.title.length}자)`, val: result.title, key: "t", mono: false, clr: "#58A6FF" },
                  { lbl: `📝 메타설명 (${result.metaDescription?.length}자)`, val: result.metaDescription, key: "m", mono: false, clr: "#C9D1D9" },
                  { lbl: "🔗 URL 슬러그", val: `/${result.slug}`, key: "s", mono: true, clr: "#7EE787" },
                ].map(it => (
                  <div key={it.key} style={{ padding: 14, border: "1.5px solid #21262D", borderRadius: 9, background: "#0D1117" }}>
                    <div style={{ fontSize: 10, fontWeight: 700, color: "#6E7681", letterSpacing: "0.08em", marginBottom: 5 }}>{it.lbl}</div>
                    <div style={{ fontSize: it.mono?12:13, color: it.clr, fontFamily: it.mono?"monospace":"inherit", background: it.mono?"#161B22":"none", padding: it.mono?"5px 9px":0, borderRadius: 5, lineHeight: 1.6 }}>{it.val}</div>
                    <button className="cpBtn" onClick={() => copy(it.val, it.key)} style={{ marginTop: 7, padding: "3px 10px", background: copied===it.key?"#238636":"#161B22", color: copied===it.key?"#FFF":"#58A6FF", borderRadius: 5, border: "none", fontSize: 11, fontWeight: 600, cursor: "pointer" }}>{copied===it.key?"✅":"복사"}</button>
                  </div>
                ))}
                <div style={{ padding: "10px 14px", background: "#0D1117", borderRadius: 9, border: "1px solid #21262D", display: "flex", gap: 5, flexWrap: "wrap", alignItems: "center" }}>
                  <span style={{ fontSize: 11, fontWeight: 700, color: "#6E7681" }}>태그:</span>
                  {result.tags?.map(t => <span key={t} style={{ padding: "2px 8px", background: "#21262D", borderRadius: 9, fontSize: 11, color: "#8B949E" }}>#{t}</span>)}
                  <button className="cpBtn" onClick={() => copy(result.tags?.join(", "),"tags")} style={{ marginLeft:"auto", padding:"3px 9px", background: copied==="tags"?"#238636":"#161B22", color: copied==="tags"?"#FFF":"#8B949E", borderRadius:5, border:"none", fontSize:11, cursor:"pointer" }}>{copied==="tags"?"✅":"태그 복사"}</button>
                </div>
              </div>
            )}

            {tab === "sns" && (
              <div style={{ padding: 18, background: "#0D1117", borderRadius: 9, border: "1.5px solid #21262D" }}>
                <div style={{ fontSize: 10, fontWeight: 700, color: "#B45309", marginBottom: 10, letterSpacing: "0.1em" }}>📲 카카오톡 · 인스타그램 · 페이스북</div>
                <div style={{ fontSize: 14, lineHeight: 1.9, color: "#C9D1D9", whiteSpace: "pre-wrap", background: "#161B22", padding: "13px 15px", borderRadius: 8, border: "1px solid #30363D" }}>{result.snsText}</div>
                <button className="cpBtn" onClick={() => copy(result.snsText,"sns")} style={{ marginTop: 10, padding: "7px 15px", background: copied==="sns"?"#238636":"#B45309", color: "#FFF", borderRadius: 7, border: "none", fontSize: 12, fontWeight: 700, cursor: "pointer" }}>{copied==="sns"?"✅ 복사됨!":"📋 SNS 텍스트 복사"}</button>
              </div>
            )}

            {tab === "wp" && (
              <div>
                <div style={{ padding: "9px 13px", background: "#051D3E", borderRadius: 8, fontSize: 12, color: "#58A6FF", marginBottom: 10, lineHeight: 1.6, border: "1px solid #1D4ED8" }}>
                  💡 워드프레스 → 글쓰기 → 우상단 <strong>⋮</strong> → <strong>코드 편집기</strong> → 전체 붙여넣기 → Yoast SEO에 메타설명 입력
                </div>
                <div style={{ background: "#0D1117", borderRadius: 9, padding: "13px 15px", fontFamily: "monospace", fontSize: 11, color: "#7EE787", lineHeight: 1.7, overflow: "auto", maxHeight: 290, whiteSpace: "pre-wrap", border: "1px solid #21262D" }}>{wpCode(result)}</div>
                <button className="cpBtn" onClick={() => copy(wpCode(result),"wp")} style={{ marginTop: 10, padding: "7px 15px", background: copied==="wp"?"#238636":"#21262D", color: copied==="wp"?"#FFF":"#C8A96E", borderRadius: 7, border: `1px solid ${copied==="wp"?"#238636":"#30363D"}`, fontSize: 12, fontWeight: 700, cursor: "pointer" }}>{copied==="wp"?"✅ 복사됨!":"📋 워드프레스 코드 복사"}</button>
              </div>
            )}
          </div>
        )}

        {/* ── HISTORY ── */}
        {history.length > 0 && (
          <div style={{ background: "#161B22", borderRadius: 13, padding: "16px 20px", border: "1px solid #30363D" }}>
            <div style={{ fontSize: 10, fontWeight: 700, color: "#6E7681", letterSpacing: "0.12em", marginBottom: 9 }}>📚 최근 생성 내역 ({history.length}건)</div>
            <div style={{ display: "grid", gap: 5 }}>
              {history.map((item, i) => {
                const c = CATS.find(x => x.id === item.cat);
                return (
                  <button key={i} onClick={() => { setResult(item.r); setKw(item.kw); setCat(item.cat); setTab("content"); setPhase("done"); }}
                    style={{ textAlign: "left", padding: "8px 11px", border: "1.5px solid #21262D", borderRadius: 8, background: "#0D1117", cursor: "pointer", display: "flex", gap: 7, alignItems: "center" }}>
                    <span style={{ fontSize: 10, padding: "2px 7px", background: c?.bg, color: c?.accent, borderRadius: 7, fontWeight: 700, whiteSpace: "nowrap" }}>{c?.emoji} {c?.label}</span>
                    <span style={{ fontSize: 12, color: "#C9D1D9", fontWeight: 500 }}>{item.r.title}</span>
                    <span style={{ fontSize: 10, color: "#6E7681", marginLeft: "auto", whiteSpace: "nowrap" }}>공고 {item.cnt}건</span>
                  </button>
                );
              })}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}
