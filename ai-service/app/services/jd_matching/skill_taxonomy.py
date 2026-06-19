"""Canonical tech-skill taxonomy used for CV<->JD matching.

Each entry maps a canonical display name to the aliases/spellings that should
resolve to it. Matching is alias-aware so "JS", "Reactjs", "k8s", or "postgres"
all collapse onto their canonical skill. Keep aliases lowercase; the extractor
lowercases input before comparing.

This is deliberately a curated dictionary (not an LLM): matching stays fast,
free, deterministic, and easy to extend. Add skills here as the domain grows.
"""

# canonical -> tuple of aliases (lowercase, includes the canonical form lowered)
SKILL_TAXONOMY: dict[str, tuple[str, ...]] = {
    # -- Languages --
    "Python": ("python",),
    "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript", "ts"),
    "Java": ("java",),
    "Kotlin": ("kotlin",),
    "Go": ("golang", "go"),
    "Rust": ("rust",),
    "C++": ("c++", "cpp"),
    "C#": ("c#", "csharp"),
    "C": ("c language", "c programming"),
    "PHP": ("php",),
    "Ruby": ("ruby",),
    "Swift": ("swift",),
    "Scala": ("scala",),
    "SQL": ("sql",),
    "Bash": ("bash", "shell scripting"),
    # -- Frontend --
    "React": ("react.js", "reactjs", "react"),
    "Next.js": ("next.js", "nextjs"),
    "Vue": ("vue.js", "vuejs", "vue"),
    "Angular": ("angular",),
    "Redux": ("redux",),
    "Tailwind": ("tailwind css", "tailwindcss", "tailwind"),
    "HTML": ("html", "html5"),
    "CSS": ("css", "css3"),
    "Jetpack Compose": ("jetpack compose",),
    # -- Backend / frameworks --
    "Node.js": ("node.js", "nodejs", "node"),
    "Express": ("express.js", "expressjs", "express"),
    "NestJS": ("nestjs", "nest.js"),
    "FastAPI": ("fastapi",),
    "Django": ("django",),
    "Flask": ("flask",),
    "Spring": ("spring boot", "spring"),
    "GraphQL": ("graphql",),
    "REST": ("rest api", "restful", "rest"),
    "gRPC": ("grpc",),
    "Prisma": ("prisma",),
    # -- Data stores --
    "PostgreSQL": ("postgresql", "postgres", "psql"),
    "MySQL": ("mysql",),
    "MongoDB": ("mongodb", "mongo"),
    "Redis": ("redis",),
    "Elasticsearch": ("elasticsearch", "elastic search"),
    "Kafka": ("kafka",),
    "RabbitMQ": ("rabbitmq",),
    # -- Cloud / DevOps --
    "AWS": ("aws", "amazon web services"),
    "GCP": ("gcp", "google cloud"),
    "Azure": ("azure",),
    "Docker": ("docker",),
    "Kubernetes": ("kubernetes", "k8s"),
    "Terraform": ("terraform",),
    "Ansible": ("ansible",),
    "CI/CD": ("ci/cd", "cicd", "continuous integration"),
    "Jenkins": ("jenkins",),
    "GitHub Actions": ("github actions",),
    "Prometheus": ("prometheus",),
    "Grafana": ("grafana",),
    "Git": ("git",),
    # -- Data / ML --
    "pandas": ("pandas",),
    "NumPy": ("numpy",),
    "scikit-learn": ("scikit-learn", "sklearn", "scikit learn"),
    "PyTorch": ("pytorch",),
    "TensorFlow": ("tensorflow",),
    "Hugging Face": ("hugging face", "huggingface"),
    "Spark": ("apache spark", "pyspark", "spark"),
    "Airflow": ("apache airflow", "airflow"),
    "MLflow": ("mlflow",),
    # -- Testing --
    "Selenium": ("selenium",),
    "Cypress": ("cypress",),
    "Playwright": ("playwright",),
    "Jest": ("jest",),
    "Pytest": ("pytest",),
    # -- Mobile --
    "Android": ("android sdk", "android"),
    "iOS": ("ios",),
    "Flutter": ("flutter",),
    "React Native": ("react native",),
}
