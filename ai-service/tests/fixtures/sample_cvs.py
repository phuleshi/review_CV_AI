"""Five sample CVs for exercising the AI Review Engine.

Deliberately varied so scores differentiate: a strong senior, a solid mid-level,
a junior leaning on projects, a weak duty-listing CV with no metrics, and a
full-stack profile.
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

SAMPLE_CVS = {
    "senior_backend": SENIOR_BACKEND,
    "mid_frontend": MID_FRONTEND,
    "junior_projects": JUNIOR_PROJECTS,
    "weak_no_metrics": WEAK_NO_METRICS,
    "fullstack": FULLSTACK,
}
