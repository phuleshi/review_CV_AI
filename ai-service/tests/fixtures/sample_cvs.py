"""Realistic sample CVs for exercising the parser and the AI Review Engine.

Deliberately varied across roles, seniority, and formatting so both the
normalizer (sections, skills, experience) and the review engine (score
differentiation) get meaningful coverage. Eleven CVs in total — well past the
"at least 10 real CVs" parser requirement.
"""

SENIOR_BACKEND = """\
John Carter
john.carter@example.com | github.com/jcarter

Summary
Senior Backend Engineer with 8 years building scalable Python and Go services.

Skills
Python, FastAPI, Go, PostgreSQL, Redis, Kafka, Docker, Kubernetes, AWS, CI/CD

Experience
Senior Backend Engineer, Acme (2020 - Present)
- Led migration to microservices, reducing p99 latency by 40%.
- Designed an event-driven pipeline processing 2,000,000 events/day.
- Improved test coverage from 45% to 90%.

Backend Engineer, Globex (2016 - 2020)
- Built REST APIs serving 500,000 monthly users.
- Optimized PostgreSQL queries, cutting report time by 60%.

Projects
- Distributed rate limiter (Go, Redis) - github.com/jcarter/ratelimit

Education
B.Sc. Computer Science
"""

MID_FRONTEND = """\
Maria Lopez
maria.lopez@example.com

Summary
Frontend Engineer focused on React and TypeScript.

Skills
JavaScript, TypeScript, React, Next.js, Tailwind, Redux, Jest

Experience
Frontend Engineer, Initech (2021 - Present)
- Built a design system used across 5 product teams.
- Improved Lighthouse performance score from 70 to 95.

Projects
- Personal portfolio (Next.js) - github.com/mlopez/portfolio

Education
B.A. Information Technology
"""

JUNIOR_PROJECTS = """\
Alex Nguyen
alex.nguyen@example.com | github.com/alexn

Summary
Recent CS graduate seeking a frontend developer role.

Skills
HTML, CSS, JavaScript, React, Git

Projects
- Weather app (React, OpenWeather API) - github.com/alexn/weather
- Task tracker (React, Node.js, MongoDB) - github.com/alexn/tasks
- Built a chat app with WebSockets, deployed on Vercel.

Education
B.Sc. Computer Science, 2024
"""

WEAK_NO_METRICS = """\
Sam Taylor
sam taylor

Work
Worked at a software company. Responsible for writing code and fixing bugs.
Was part of a team that handled various tasks. Helped with different projects.
Responsible for maintaining the website and other duties as assigned.

Education
Studied computer science.
"""

FULLSTACK = """\
Priya Sharma
priya.sharma@example.com | github.com/priyash

Summary
Full-stack engineer comfortable across React frontends and Node/Nest backends.

Skills
TypeScript, React, Next.js, NestJS, Node.js, PostgreSQL, Prisma, Docker, AWS, GraphQL

Experience
Full-Stack Engineer, Hooli (2021 - Present)
- Shipped a billing module end-to-end, increasing conversion by 18%.
- Built typed REST + GraphQL APIs consumed by the React app.

Projects
- Open-source CV reviewer (Next.js + NestJS + Postgres) - github.com/priyash/cv

Education
B.Eng. Software Engineering
"""

DATA_SCIENTIST = """\
Daniel Kim
daniel.kim@example.com | +1 (415) 555-0147 | linkedin.com/in/danielkim

Summary
Data Scientist with 5 years turning messy data into production ML.

Technical Skills
Python, pandas, NumPy, scikit-learn, PyTorch, SQL, Spark, Airflow, AWS SageMaker

Experience
Senior Data Scientist, DataCorp (2021 - Present)
- Built a churn model that cut customer churn by 12%.
- Deployed 6 ML pipelines serving 1,000,000 predictions/day.

Data Analyst, Metrics Inc (2019 - 2021)
- Automated reporting, saving 20 hours/week of manual work.

Projects
- Fraud detection pipeline (Python, XGBoost, Kafka) - github.com/dkim/fraud

Education
M.Sc. Statistics, Stanford University, 2019

Certifications
AWS Certified Machine Learning - Specialty
TensorFlow Developer Certificate
"""

DEVOPS_ENGINEER = """\
Olivia Brown
olivia.brown@example.com | github.com/obrown

Summary
DevOps Engineer automating infrastructure for high-availability systems.

Skills
Terraform, Kubernetes, Docker, AWS, GCP, Ansible, Prometheus, Grafana, Bash, Python, CI/CD

Experience
DevOps Engineer, CloudScale (2020 - Present)
- Migrated 40 services to Kubernetes, improving uptime to 99.95%.
- Cut deployment time from 45 minutes to 6 minutes with GitOps.

Systems Engineer, HostingCo (2017 - 2020)
- Managed 200+ Linux servers and on-call incident response.

Education
B.Sc. Computer Engineering

Certifications
Certified Kubernetes Administrator (CKA)
AWS Certified Solutions Architect - Associate
"""

MOBILE_DEVELOPER = """\
Hiroshi Tanaka
hiroshi.tanaka@example.com | github.com/htanaka

Summary
Android Engineer shipping consumer apps with millions of installs.

Skills
Kotlin, Java, Android SDK, Jetpack Compose, Coroutines, Retrofit, Room, Firebase, Gradle

Experience
Senior Android Engineer, AppWorks (2019 - Present)
- Rebuilt the app in Jetpack Compose, cutting crash rate by 35%.
- Grew Play Store rating from 3.8 to 4.6 across 2,000,000 users.

Android Developer, MobileStart (2016 - 2019)
- Shipped offline-first sync used by 300,000 monthly users.

Projects
- Habit tracker (Kotlin, Compose, Room) - github.com/htanaka/habits

Education
B.Sc. Software Engineering
"""

QA_ENGINEER = """\
Fatima Al-Sayed
fatima.alsayed@example.com

Summary
QA Automation Engineer focused on reliable end-to-end test coverage.

Skills
Selenium, Cypress, Playwright, Python, JavaScript, Postman, JMeter, Jenkins, Git

Experience
QA Automation Engineer, TestLabs (2020 - Present)
- Built an E2E suite of 800 tests, raising release confidence.
- Reduced regression cycle from 3 days to 4 hours.

Manual QA Tester, SoftCo (2018 - 2020)
- Authored test plans and tracked defects across 4 product lines.

Education
B.Sc. Information Systems

Certifications
ISTQB Certified Tester - Foundation Level
"""

ML_ENGINEER = """\
Carlos Mendes
carlos.mendes@example.com | github.com/cmendes | linkedin.com/in/cmendes

Summary
Machine Learning Engineer bridging research and scalable production systems.

Technical Skills
Python, PyTorch, TensorFlow, Hugging Face, FastAPI, Ray, Kubernetes, MLflow, AWS

Experience
ML Engineer, VisionAI (2021 - Present)
- Served a transformer model at 50ms p95 latency under 10k QPS.
- Reduced inference cost by 30% via quantization and batching.

Research Engineer, DeepLab (2019 - 2021)
- Published 2 papers on efficient training and contributed to open-source.

Projects
- LLM serving framework (Python, Ray, FastAPI) - github.com/cmendes/serve

Education
M.Sc. Computer Science, 2019

Certifications
Deep Learning Specialization (Coursera)
"""

PRODUCT_MANAGER = """\
Emma Wilson
emma.wilson@example.com | linkedin.com/in/emmawilson

Summary
Product Manager with 6 years shipping B2B SaaS that customers love.

Skills
Product Strategy, Roadmapping, User Research, A/B Testing, SQL, Jira, Figma, Analytics

Experience
Senior Product Manager, SaaSly (2020 - Present)
- Launched a self-serve onboarding flow that lifted activation by 25%.
- Drove a $4M ARR feature from discovery to GA in 9 months.

Product Manager, GrowthHub (2017 - 2020)
- Ran 30+ experiments, improving trial-to-paid conversion by 14%.

Education
MBA, Business Administration
B.A. Economics
"""

SAMPLE_CVS = {
    "senior_backend": SENIOR_BACKEND,
    "mid_frontend": MID_FRONTEND,
    "junior_projects": JUNIOR_PROJECTS,
    "weak_no_metrics": WEAK_NO_METRICS,
    "fullstack": FULLSTACK,
    "data_scientist": DATA_SCIENTIST,
    "devops_engineer": DEVOPS_ENGINEER,
    "mobile_developer": MOBILE_DEVELOPER,
    "qa_engineer": QA_ENGINEER,
    "ml_engineer": ML_ENGINEER,
    "product_manager": PRODUCT_MANAGER,
}
