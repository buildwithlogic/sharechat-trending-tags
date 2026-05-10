from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from services.trend_service import get_trending_tags_service
from schemas.trend_schema import TrendingTag

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Trending Tags API is running"}


@app.get("/trending-tags", response_model=list[TrendingTag])
def get_trending_tags():
    return get_trending_tags_service()


@app.get("/app", response_class=HTMLResponse)
def trending_app():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Trending Tags</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <style>
            * {
                box-sizing: border-box;
            }

            body {
                margin: 0;
                font-family: Inter, Arial, sans-serif;
                background: linear-gradient(180deg, #fff7ed 0%, #f8fafc 35%, #eef2ff 100%);
                color: #111827;
            }

            .app-container {
                max-width: 430px;
                margin: 0 auto;
                min-height: 100vh;
                padding: 18px 14px 28px;
            }

            .top-banner {
                background: linear-gradient(135deg, #f97316, #ec4899);
                color: white;
                border-radius: 24px;
                padding: 20px 18px;
                box-shadow: 0 10px 30px rgba(236, 72, 153, 0.18);
                margin-bottom: 18px;
            }

            .header {
                font-size: 32px;
                font-weight: 800;
                line-height: 1.05;
                margin-bottom: 8px;
                letter-spacing: -0.5px;
            }

            .subheader {
                font-size: 14px;
                line-height: 1.5;
                color: rgba(255, 255, 255, 0.92);
            }

            .section-title {
                font-size: 14px;
                font-weight: 700;
                color: #6b7280;
                margin: 8px 4px 14px;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            }

            .trend-card {
                background: rgba(255, 255, 255, 0.9);
                backdrop-filter: blur(6px);
                border: 1px solid rgba(255, 255, 255, 0.7);
                border-radius: 22px;
                padding: 16px;
                margin-bottom: 14px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
                transition: transform 0.18s ease, box-shadow 0.18s ease;
                cursor: pointer;
            }

            .trend-card:hover {
                transform: translateY(-2px);
                box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
            }

            .trend-top-row {
                display: flex;
                align-items: flex-start;
                justify-content: space-between;
                gap: 10px;
                margin-bottom: 10px;
            }

            .tag {
                font-size: 24px;
                font-weight: 800;
                line-height: 1.2;
                color: #1f2937;
                word-break: break-word;
            }

            .right-badges {
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                gap: 8px;
                flex-shrink: 0;
            }

            .heat-badge {
                background: #111827;
                color: white;
                font-size: 12px;
                font-weight: 700;
                padding: 7px 10px;
                border-radius: 999px;
            }

            .traffic-badge {
                background: #fef3c7;
                color: #92400e;
                font-size: 12px;
                font-weight: 700;
                padding: 7px 10px;
                border-radius: 999px;
            }

            .description {
                font-size: 15px;
                line-height: 1.5;
                color: #4b5563;
                margin-bottom: 14px;
            }

            .meta-row {
                display: flex;
                justify-content: space-between;
                align-items: center;
                gap: 12px;
            }

            .category-pill {
                display: inline-flex;
                align-items: center;
                padding: 7px 12px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 700;
                background: #eef2ff;
                color: #4338ca;
                text-transform: capitalize;
            }

            .source-text {
                font-size: 12px;
                color: #6b7280;
                text-align: right;
            }

            .loading {
                color: #6b7280;
                font-size: 14px;
                padding: 12px 4px;
            }

            .hidden {
                display: none;
            }

            .back-button {
                border: none;
                background: white;
                color: #111827;
                border-radius: 999px;
                padding: 10px 14px;
                font-size: 14px;
                font-weight: 700;
                box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
                margin-bottom: 16px;
                cursor: pointer;
            }

            .detail-card {
                background: rgba(255, 255, 255, 0.92);
                border-radius: 24px;
                padding: 20px;
                box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.7);
            }

            .detail-tag {
                font-size: 30px;
                font-weight: 800;
                line-height: 1.15;
                margin-bottom: 12px;
                word-break: break-word;
            }

            .detail-description {
                font-size: 16px;
                line-height: 1.6;
                color: #4b5563;
                margin-bottom: 18px;
            }

            .detail-grid {
                display: grid;
                gap: 12px;
            }

            .detail-item {
                background: #f8fafc;
                border-radius: 16px;
                padding: 14px;
                border: 1px solid #e5e7eb;
            }

            .detail-label {
                font-size: 12px;
                font-weight: 700;
                color: #6b7280;
                text-transform: uppercase;
                letter-spacing: 0.06em;
                margin-bottom: 6px;
            }

            .detail-value {
                font-size: 15px;
                font-weight: 600;
                color: #111827;
                word-break: break-word;
            }
        </style>
    </head>
    <body>
        <div class="app-container">
            <div id="list-screen">
                <div class="top-banner">
                    <div class="header">Trending in India</div>
                    <div class="subheader">
                        Discover what people across India are searching for right now.
                    </div>
                </div>

                <div class="section-title">Top live tags</div>
                <div id="trend-list" class="loading">Loading trends...</div>
            </div>

            <div id="detail-screen" class="hidden">
                <button class="back-button" onclick="showListScreen()">← Back</button>

                <div class="detail-card">
                    <div id="detail-tag" class="detail-tag"></div>
                    <div id="detail-description" class="detail-description"></div>

                    <div class="detail-grid">
                        <div class="detail-item">
                            <div class="detail-label">Category</div>
                            <div id="detail-category" class="detail-value"></div>
                        </div>

                        <div class="detail-item">
                            <div class="detail-label">Heat</div>
                            <div id="detail-heat" class="detail-value"></div>
                        </div>

                        <div class="detail-item">
                            <div class="detail-label">Approx Traffic</div>
                            <div id="detail-traffic" class="detail-value"></div>
                        </div>

                        <div class="detail-item">
                            <div class="detail-label">Source</div>
                            <div id="detail-source" class="detail-value"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let allTrends = [];

            function getHeatLabel(score) {
                if (score >= 95) return "Top Trend";
                if (score >= 85) return "Hot";
                if (score >= 70) return "Picking Up";
                return "Emerging";
            }

            function showDetailScreen(index) {
                const trend = allTrends[index];

                document.getElementById('detail-tag').textContent = trend.tag;
                document.getElementById('detail-description').textContent = trend.description;
                document.getElementById('detail-category').textContent = trend.category;
                document.getElementById('detail-heat').textContent = `${getHeatLabel(trend.heat_score)} (${trend.heat_score})`;
                document.getElementById('detail-traffic').textContent = trend.approx_traffic || 'Not available';
                document.getElementById('detail-source').textContent = trend.source;

                document.getElementById('list-screen').classList.add('hidden');
                document.getElementById('detail-screen').classList.remove('hidden');
                window.scrollTo(0, 0);
            }

            function showListScreen() {
                document.getElementById('detail-screen').classList.add('hidden');
                document.getElementById('list-screen').classList.remove('hidden');
                window.scrollTo(0, 0);
            }

            async function loadTrends() {
                const response = await fetch('/trending-tags');
                const trends = await response.json();
                allTrends = trends;

                const trendList = document.getElementById('trend-list');

                if (!trends.length) {
                    trendList.innerHTML = "<div class='loading'>No trends available</div>";
                    return;
                }

                trendList.innerHTML = trends.map((trend, index) => `
                    <div class="trend-card" onclick="showDetailScreen(${index})">
                        <div class="trend-top-row">
                            <div class="tag">${trend.tag}</div>
                            <div class="right-badges">
                                <div class="heat-badge">${getHeatLabel(trend.heat_score)} · ${trend.heat_score}</div>
                                <div class="traffic-badge">${trend.approx_traffic || 'N/A'}</div>
                            </div>
                        </div>

                        <div class="description">${trend.description}</div>

                        <div class="meta-row">
                            <span class="category-pill">${trend.category}</span>
                            <span class="source-text">${trend.source}</span>
                        </div>
                    </div>
                `).join('');
            }

            loadTrends();
        </script>
    </body>
    </html>
    """
