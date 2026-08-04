# FIELD-CAMP-1st-Place

## 🏆 [2026 FIELD CAMP 최우수상] 기상-발전 데이터 관계 추론 기반 풍력 발전량 예측 및 AI 데이터센터 입지 최적화

### 🚀 AI 데이터센터 최적 입지 선정 및 풍력 발전량 기반 ESS 운영 파이프라인

본 프로젝트는 <b>SCADA 및 기상 데이터를 활용한 풍력 발전량 예측(Phase 2)</b>과 <b>예측된 풍력 잉여전력을 연계한 경주시 AI 데이터센터 최적 입지 선정 및 ESS(에너지저장장치) 용량 최적화(Phase 3)</b>를 통합한 End-to-End 에너지-데이터센터 최적화 파이프라인입니다.
---

## 📋 Table of Contents

- [1. 프로젝트 개요](#1-프로젝트-개요)
- [2. 기술 스택](#2-기술-스택)
- [3. 디렉토리 구조](#3-디렉토리-구조)
- [4. 파이프라인 상세](#4-파이프라인-상세)
  - [Phase 2: 풍력 발전량 예측 모델링](#phase-2-풍력-발전량-예측-모델링)
  - [Phase 3: AI 데이터센터 입지 및 ESS 최적화](#phase-3-ai-데이터센터-입지-및-ess-최적화)
- [5. 핵심 분석 인사이트 & Lessons Learned](#5-핵심-분석-인사이트--lessons-learned)
- [6. 환경 설정 및 실행 방법](#6-환경-설정-및-실행-방법)

---

## 1. 프로젝트 개요

* **프로젝트명**: AI 데이터센터 입지 최적화 및 풍력 발전량 기반 ESS 운영 파이프라인
* **주요 목적**:
  * **Phase 2**: SCADA 센서 데이터 및 환경 변수를 활용하여 12월 10분 단위 유효전력생산량(kWh)을 고도화된 머신러닝 모델로 예측.
  * **Phase 3**: 예측된 풍력 잉여전력 프로파일을 바탕으로 경주시 내 최적 부지를 선정하고, Gurobi 수리 최적화를 통해 AI 데이터센터 전력 충당을 위한 ESS 용량을 산정.

---

## 2. 기술 스택

| 구 분 | 기술 / 라이브러리 |
| :--- | :--- |
| **언어** | Python 3.12+ |
| **데이터 처리** | Pandas, NumPy |
| **머신러닝 / 예측** | LightGBM, Optuna, Scikit-learn |
| **수리 최적화** | Gurobi (`gurobipy`) |
| **시각화** | Matplotlib, Seaborn |

---

## 3. 디렉토리 구조

```text
├── data/
│   ├── train_1월_11월_.csv             # Phase 2 학습용 SCADA 데이터
│   ├── train_12월_.csv                 # Phase 2 평가/예측 대상 데이터
│   ├── terrain_grid_100m.csv          # 경주시 100m x 100m 격자 데이터
│   ├── substation_locations.csv       # 변전소 위치 및 Capacity 데이터
│   └── gyeongju_boundary.csv          # 경주시 지리적 경계 데이터
├── Phase2_Task2_LGBM_Prediction.ipynb # Phase 2 풍력 발전량 예측 노트북
├── Phase3_Siting_ESS_Optimization.ipynb # Phase 3 입지 및 ESS 최적화 노트북
├── outputs/
│   ├── Phase2_Task2_평가셋예측.csv      # Phase 2 최종 예측 결과
│   └── phase3_outputs/                # Phase 3 최종 부지 리포트 및 시각화 그래프
└── README.md                          # 프로젝트 안내 문서
---

## 4. 파이프라인 상세

### ⚙️ Phase 2: 풍력 발전량 예측 모델링 (`Task 2`)

1. **문제 정의 및 데이터 전처리**
   - 1~11월 실측 데이터를 기반으로 12월 평가셋의 10분 단위 유효전력생산량 예측.
   - 마스킹된 `Feature_1~18` 컬럼을 도메인 지식 기반으로 재식별 (나셀 풍속, 나셀 풍향 sin/cos, 기온, 기압, 로터 회전수 등).

2. **피처 엔지니어링 (Feature Engineering)**
   - **물리 기반 파생변수**:
     - 이상기체 상태방정식 기반 공기밀도(`air_density_calc`)
     - Betz 이론 기반 풍력 에너지 플럭스(`wind_power_flux`)
     - 요 정렬 오차 (`yaw_misalign_cos/deg`) 및 유효 풍속
   - **시간/계절 순환 피처**: 외삽 위험을 차단하기 위해 연월일 단순 달력 변수를 제거하고 순환 인코딩(`hour_sin/cos`, `doy_sin/cos`) 적용.

3. **Data Leakage 차단 및 검증 전략**
   - **Leakage 변수 제거**: `op_switch`, `forced_stop_min`, `normal_op_min` 등 예측 시점 이후에만 알 수 있는 사후 집계 컬럼 제거.
   - **Walk-forward CV**: 시계열 구조에 맞춰 Walk-forward Cross-Validation (1-8월 학습 → 9월 검증 , 1-9월 학습 → 10월 검증 등) 구축.

4. **특수 패턴 발굴 및 모델 채택**
   - **70일 정비 주기 패턴**: 100시간 이상 무발전 구간 전수 분석 결과 70일 주기 정비 패턴(5/20, 7/29, 10/7 → 12/16 정비) 발굴 및 위상 피처 반영.
   - **극저온 성능 저하**: -10℃ 이하 극저온 환경에서의 출력 저하 패턴 반영 (`extreme_cold_flag`, `cold_severity`).
   - **최종 모델 (v6)**: 실증 평가셋(12월) 기준 <b>v6 모델(NMAE 0.0934)</b>을 최종 제출 모델로 채택.

---

### 🏛️ Phase 3: AI 데이터센터 입지 및 ESS 최적화

1. **후보지 생성 및 제약조건 (Candidate Generation)**
   - **격자 필터링**: 경주시 100m × 100m 격자(총 90,000개 셀) 대상 공간 필터링:
     - 경주시 행정구역 내부 영역
     - 경사도 15도 이하 안전 지형
     - 문화재 보호 구역 버퍼 외부
     - 3개 변전소(경주, 입실, 양북) 최소 안전 이격거리 2.07071km 이상 확보
   - **부지 형상 및 인구지표**: 30MW(3개 형상) 및 50MW(5개 형상) 직사각형 후보지 약 309,533개 생성. 인구 지표는 상대적 백분위 점수(`population_score`)로 정규화.

2. **풍력 잉여전력 프로파일 연계**
   - Phase 2 예측 결과(7기 풍력터빈 10분 단위 발전량) 기반 70% 잉여전력(MW) 프로파일 생성 및 최적화 연동.

3. **Gurobi 기반 Multi-Stage Optimization**
   - **Stage 1 (부지 최적 선정)**:
     - 예산 한도, 변전소 용량 제한, 송전선 설치 예산, 격자 중첩 방지 제약 반영.
     - 계층적 다목적 함수: 1순위 경사등급 최소화 → 2순위 송전선 비용 최소화 → 3순위 인구지표 백분위 최소화.
   - **Stage 2 (ESS 용량 산정 및 시뮬레이션)**:
     - AI 데이터센터 전력 충당률 극대화 및 미충당 전력 최소화를 위한 ESS 최적 용량 산정.
     - 예산 증설 시나리오별 수리적 시뮬레이션 수행.

---

## 5. 핵심 분석 인사이트 & Lessons Learned

1. **Leakage 컬럼의 역발상 활용 (EDA/기초 분석)**
   - `강제정지시간(분)` 등 사후 데이터는 예측 피처로 직접 사용할 경우 Data Leakage가 발생하지만, **탐색적 분석(EDA)의 타깃**으로 활용하여 저기압 threshold 및 특정 남-남서풍 폭풍 방향 등의 물리적 특성을 추정하는 핵심 열쇠로 활용함.
2. **CV 점수와 Test NMAE 간의 괴리 대응**
   - 겨울철 데이터 부재로 인해 단순 CV 점수에만 의존할 경우 오버피팅 발생 위험 확인. 실증 테스트 NMAE를 지속 점검하여 과도한 복잡도를 가진 v9 모델 대신 일반화 성능이 뛰어난 v6 모델을 선별 채택함.

---

## 6. 환경 설정 및 실행 방법

### ⚙️ Prerequisites

- Python 3.12 이상
- **Gurobi Optimizer**: Phase 3 실행을 위해 유효한 Gurobi 라이선스(Academic/Commercial) 설치 필요

### 💻 Installation

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
pip install pandas numpy lightgbm optuna scikit-learn gurobipy matplotlib seaborn
