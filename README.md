# FIELD-CAMP-1st-Place
[2026 FIELD CAMP 최우수상] 기상-발전 데이터 관계 추론 기반 풍력 발전량 예측 및 AI 데이터센터 입지 최적화

# 🚀 AI 데이터센터 최적 입지 선정 및 풍력 발전량 기반 ESS 운영 파이프라인

본 프로젝트는 **SCADA 및 기상 데이터를 활용한 풍력 발전량 예측(Phase 2)**과 **예측된 풍력 잉여전력을 연계한 경주시 AI 데이터센터 최적 입지 선정 및 ESS(에너지저장장치) 용량 최적화(Phase 3)**를 통합한 End-to-End 에너지-데이터센터 최적화 파이프라인입니다.

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

└── README.md   
