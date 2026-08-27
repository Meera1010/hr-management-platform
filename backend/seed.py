from app import create_app, db
from app.models.role import Role
from app.models.user import User

def seed_database():
    app = create_app()
    with app.app_context():
        # 1. Create tables
        db.create_all()

        # 2. Create roles if they don't exist
        default_roles = ['Admin', 'HR', 'Recruiter', 'Employee', 'Candidate', 'Interviewer']
        
        for role_name in default_roles:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                role = Role(name=role_name, description=f"{role_name} role")
                db.session.add(role)
        db.session.commit()
        print("Roles seeded.")



        # 4. Create a few demo users
        demo_users = [
            {'first': 'Demo', 'last': 'Admin', 'email': 'admin@example.com', 'role': 'Admin', 'pass': 'demo-password'},
            {'first': 'Demo', 'last': 'HR', 'email': 'hr@example.com', 'role': 'HR', 'pass': 'demo-password'},
            {'first': 'Demo', 'last': 'Recruiter', 'email': 'recruiter@example.com', 'role': 'Recruiter', 'pass': 'demo-password'},
            {'first': 'Demo', 'last': 'Employee', 'email': 'employee@example.com', 'role': 'Employee', 'pass': 'demo-password'},
            {'first': 'Demo', 'last': 'Candidate', 'email': 'candidate@example.com', 'role': 'Candidate', 'pass': 'demo-password'},
            {'first': 'Demo', 'last': 'Interviewer', 'email': 'interviewer@example.com', 'role': 'Interviewer', 'pass': 'demo-password'}
        ]
        
        for u in demo_users:
            user = User.query.filter_by(email=u['email']).first()
            if not user:
                r = Role.query.filter_by(name=u['role']).first()
                user = User(
                    first_name=u['first'],
                    last_name=u['last'],
                    email=u['email'],
                    role_id=r.id
                )
                user.set_password(u['pass'])
                db.session.add(user)
            else:
                user.set_password(u['pass']) # Ensure password is up to date for demo
        db.session.commit()
        print("Demo users seeded.")

        # 5. Create fictional departments
        from app.models.department import Department
        from app.models.employee import Employee
        from datetime import datetime

        fictional_departments = [
            {'name': 'Engineering', 'desc': 'Software engineering and development'},
            {'name': 'Human Resources', 'desc': 'HR and talent acquisition'},
            {'name': 'Marketing', 'desc': 'Marketing and brand management'},
            {'name': 'Finance', 'desc': 'Accounting and finance'},
            {'name': 'Operations', 'desc': 'Company operations and logistics'}
        ]

        dept_map = {}
        for fd in fictional_departments:
            dept = Department.query.filter_by(name=fd['name']).first()
            if not dept:
                dept = Department(name=fd['name'], description=fd['desc'], status='Active')
                db.session.add(dept)
                db.session.commit()
            dept_map[dept.name] = dept.id
        print("Departments seeded.")

        # 6. Create fictional employees mapped to users if available
        fictional_employees = [
            {'code': 'EMP001', 'first': 'Alex', 'last': 'Kumar', 'email': 'employee001@example.com', 'dept': 'Engineering', 'desig': 'Software Engineer', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP002', 'first': 'Jordan', 'last': 'Smith', 'email': 'employee002@example.com', 'dept': 'Engineering', 'desig': 'Senior Engineer', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP003', 'first': 'Taylor', 'last': 'Wilson', 'email': 'employee003@example.com', 'dept': 'Human Resources', 'desig': 'HR Specialist', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP004', 'first': 'Casey', 'last': 'Jones', 'email': 'employee004@example.com', 'dept': 'Marketing', 'desig': 'Marketing Manager', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP005', 'first': 'Jamie', 'last': 'Lee', 'email': 'employee005@example.com', 'dept': 'Finance', 'desig': 'Financial Analyst', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP006', 'first': 'Avery', 'last': 'Davis', 'email': 'employee006@example.com', 'dept': 'Operations', 'desig': 'Operations Coordinator', 'type': 'Contract', 'role': 'Employee'},
            {'code': 'EMP007', 'first': 'Riley', 'last': 'Martin', 'email': 'employee007@example.com', 'dept': 'Engineering', 'desig': 'QA Engineer', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP008', 'first': 'Quinn', 'last': 'White', 'email': 'employee008@example.com', 'dept': 'Marketing', 'desig': 'SEO Specialist', 'type': 'Part Time', 'role': 'Employee'},
            {'code': 'EMP009', 'first': 'Skyler', 'last': 'Hall', 'email': 'employee009@example.com', 'dept': 'Human Resources', 'desig': 'Recruiter', 'type': 'Full Time', 'role': 'Recruiter'},
            {'code': 'EMP010', 'first': 'Cameron', 'last': 'Allen', 'email': 'employee010@example.com', 'dept': 'Engineering', 'desig': 'DevOps Engineer', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP011', 'first': 'Drew', 'last': 'Young', 'email': 'employee011@example.com', 'dept': 'Operations', 'desig': 'Logistics Manager', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP012', 'first': 'Reese', 'last': 'King', 'email': 'employee012@example.com', 'dept': 'Finance', 'desig': 'Accountant', 'type': 'Full Time', 'role': 'Employee'},
            {'code': 'EMP013', 'first': 'Morgan', 'last': 'Wright', 'email': 'employee013@example.com', 'dept': 'Engineering', 'desig': 'Frontend Developer', 'type': 'Intern', 'role': 'Employee'},
            {'code': 'EMP014', 'first': 'Logan', 'last': 'Scott', 'email': 'employee014@example.com', 'dept': 'Marketing', 'desig': 'Content Creator', 'type': 'Contract', 'role': 'Employee'},
            {'code': 'EMP015', 'first': 'Rowan', 'last': 'Green', 'email': 'employee015@example.com', 'dept': 'Engineering', 'desig': 'Backend Developer', 'type': 'Full Time', 'role': 'Employee'},
            # Adding the generic demo employee to employee table
            {'code': 'EMP000', 'first': 'Demo', 'last': 'Employee', 'email': 'employee@example.com', 'dept': 'Engineering', 'desig': 'Demo Employee', 'type': 'Full Time', 'role': 'Employee'}
        ]

        employee_role = Role.query.filter_by(name='Employee').first()
        recruiter_role = Role.query.filter_by(name='Recruiter').first()

        for fe in fictional_employees:
            # 6.a Add user if not exists
            user = User.query.filter_by(email=fe['email']).first()
            if not user:
                role_to_assign = employee_role if fe['role'] == 'Employee' else recruiter_role
                user = User(
                    first_name=fe['first'],
                    last_name=fe['last'],
                    email=fe['email'],
                    role_id=role_to_assign.id
                )
                user.set_password('demo-password')
                db.session.add(user)
                db.session.commit()
            
            # 6.b Add employee
            emp = Employee.query.filter_by(employee_code=fe['code']).first()
            if not emp:
                emp = Employee(
                    employee_code=fe['code'],
                    first_name=fe['first'],
                    last_name=fe['last'],
                    email=fe['email'],
                    phone='555-0100',
                    department_id=dept_map[fe['dept']],
                    user_id=user.id,
                    designation=fe['desig'],
                    joining_date=datetime.strptime('2023-01-15', '%Y-%m-%d').date(),
                    employment_type=fe['type'],
                    status='Active'
                )
                db.session.add(emp)
        db.session.commit()
        print("Fictional employees seeded.")

        # 7. Create fictional jobs
        from app.models.job import Job
        fictional_jobs = [
            {'code': 'JOB001', 'title': 'Senior Software Engineer', 'dept': 'Engineering', 'type': 'Full Time', 'location': 'Remote', 'status': 'Open'},
            {'code': 'JOB002', 'title': 'Frontend Developer', 'dept': 'Engineering', 'type': 'Full Time', 'location': 'New York', 'status': 'Open'},
            {'code': 'JOB003', 'title': 'HR Specialist', 'dept': 'Human Resources', 'type': 'Full Time', 'location': 'London', 'status': 'Open'},
            {'code': 'JOB004', 'title': 'Marketing Manager', 'dept': 'Marketing', 'type': 'Full Time', 'location': 'Remote', 'status': 'Open'},
            {'code': 'JOB005', 'title': 'Financial Analyst', 'dept': 'Finance', 'type': 'Full Time', 'location': 'San Francisco', 'status': 'Closed'},
            {'code': 'JOB006', 'title': 'Operations Coordinator', 'dept': 'Operations', 'type': 'Contract', 'location': 'Austin', 'status': 'Open'},
            {'code': 'JOB007', 'title': 'QA Engineer', 'dept': 'Engineering', 'type': 'Full Time', 'location': 'Remote', 'status': 'Draft'},
            {'code': 'JOB008', 'title': 'SEO Specialist', 'dept': 'Marketing', 'type': 'Part Time', 'location': 'Chicago', 'status': 'Open'},
            {'code': 'JOB009', 'title': 'Recruiter', 'dept': 'Human Resources', 'type': 'Full Time', 'location': 'Boston', 'status': 'Open'},
            {'code': 'JOB010', 'title': 'DevOps Engineer', 'dept': 'Engineering', 'type': 'Full Time', 'location': 'Remote', 'status': 'Archived'}
        ]
        
        admin_user = User.query.filter_by(email='admin@example.com').first()
        for fj in fictional_jobs:
            job = Job.query.filter_by(job_code=fj['code']).first()
            if not job:
                job = Job(
                    job_code=fj['code'],
                    title=fj['title'],
                    department_id=dept_map[fj['dept']],
                    description=f"We are looking for a {fj['title']} to join our team.",
                    employment_type=fj['type'],
                    location=fj['location'],
                    status=fj['status'],
                    created_by=admin_user.id if admin_user else None
                )
                db.session.add(job)
        db.session.commit()
        print("Fictional jobs seeded.")

        # 8. Create fictional candidates
        from app.models.candidate import Candidate
        
        fictional_candidates = [
            {'code': 'CAN-001', 'first': 'Alex', 'last': 'Kumar', 'email': 'candidate001@example.com', 'edu': 'BSc Computer Science', 'exp': 2, 'role': 'Junior Developer', 'skills': 'Python, JavaScript, SQL', 'status': 'Available', 'loc': 'New York'},
            {'code': 'CAN-002', 'first': 'Jordan', 'last': 'Smith', 'email': 'candidate002@example.com', 'edu': 'MSc Software Engineering', 'exp': 5, 'role': 'Backend Developer', 'skills': 'Python, Django, Flask', 'status': 'Available', 'loc': 'Remote'},
            {'code': 'CAN-003', 'first': 'Taylor', 'last': 'Wilson', 'email': 'candidate003@example.com', 'edu': 'BA Business', 'exp': 3, 'role': 'HR Assistant', 'skills': 'Communication, Sourcing', 'status': 'Available', 'loc': 'London'},
            {'code': 'CAN-004', 'first': 'Casey', 'last': 'Jones', 'email': 'candidate004@example.com', 'edu': 'BSc Marketing', 'exp': 4, 'role': 'Marketing Coordinator', 'skills': 'SEO, Content Creation', 'status': 'Available', 'loc': 'Remote'},
            {'code': 'CAN-005', 'first': 'Jamie', 'last': 'Lee', 'email': 'candidate005@example.com', 'edu': 'BSc Finance', 'exp': 6, 'role': 'Senior Analyst', 'skills': 'Excel, Financial Modeling', 'status': 'Inactive', 'loc': 'San Francisco'},
            {'code': 'CAN-006', 'first': 'Avery', 'last': 'Davis', 'email': 'candidate006@example.com', 'edu': 'High School', 'exp': 1, 'role': 'Clerk', 'skills': 'Data Entry', 'status': 'Available', 'loc': 'Austin'},
            {'code': 'CAN-007', 'first': 'Riley', 'last': 'Martin', 'email': 'candidate007@example.com', 'edu': 'BSc Computer Science', 'exp': 3, 'role': 'QA Tester', 'skills': 'Manual Testing, Selenium', 'status': 'Hired', 'loc': 'Remote'},
            {'code': 'CAN-008', 'first': 'Quinn', 'last': 'White', 'email': 'candidate008@example.com', 'edu': 'MSc Marketing', 'exp': 7, 'role': 'Marketing Manager', 'skills': 'Strategy, SEO, SEM', 'status': 'Available', 'loc': 'Chicago'},
            {'code': 'CAN-009', 'first': 'Skyler', 'last': 'Hall', 'email': 'candidate009@example.com', 'edu': 'BA Human Resources', 'exp': 4, 'role': 'Talent Sourcer', 'skills': 'LinkedIn, Boolean Search', 'status': 'Rejected', 'loc': 'Boston'},
            {'code': 'CAN-010', 'first': 'Cameron', 'last': 'Allen', 'email': 'candidate010@example.com', 'edu': 'BSc IT', 'exp': 5, 'role': 'SysAdmin', 'skills': 'Linux, Bash, Docker', 'status': 'Available', 'loc': 'Remote'},
            {'code': 'CAN-011', 'first': 'Drew', 'last': 'Young', 'email': 'candidate011@example.com', 'edu': 'BSc Logistics', 'exp': 8, 'role': 'Logistics Specialist', 'skills': 'Supply Chain, Negotiation', 'status': 'Available', 'loc': 'Miami'},
            {'code': 'CAN-012', 'first': 'Reese', 'last': 'King', 'email': 'candidate012@example.com', 'edu': 'BBA Accounting', 'exp': 3, 'role': 'Junior Accountant', 'skills': 'QuickBooks, Reconciliation', 'status': 'Available', 'loc': 'Dallas'},
            {'code': 'CAN-013', 'first': 'Morgan', 'last': 'Wright', 'email': 'candidate013@example.com', 'edu': 'Bootcamp Graduate', 'exp': 0, 'role': 'Intern', 'skills': 'HTML, CSS, React', 'status': 'Available', 'loc': 'Remote'},
            {'code': 'CAN-014', 'first': 'Logan', 'last': 'Scott', 'email': 'candidate014@example.com', 'edu': 'BA English', 'exp': 2, 'role': 'Copywriter', 'skills': 'Copywriting, Editing', 'status': 'Inactive', 'loc': 'Seattle'},
            {'code': 'CAN-015', 'first': 'Rowan', 'last': 'Green', 'email': 'candidate015@example.com', 'edu': 'MSc Computer Science', 'exp': 10, 'role': 'Software Architect', 'skills': 'System Design, Microservices', 'status': 'Hired', 'loc': 'Remote'},
            {'code': 'CAN-016', 'first': 'Sam', 'last': 'Baker', 'email': 'candidate016@example.com', 'edu': 'BSc Computer Science', 'exp': 4, 'role': 'Data Analyst', 'skills': 'SQL, Python, Tableau', 'status': 'Available', 'loc': 'New York'},
            {'code': 'CAN-017', 'first': 'Chris', 'last': 'Evans', 'email': 'candidate017@example.com', 'edu': 'BSc Engineering', 'exp': 2, 'role': 'Support Engineer', 'skills': 'Troubleshooting, Zendesk', 'status': 'Available', 'loc': 'Remote'},
            {'code': 'CAN-018', 'first': 'Pat', 'last': 'Murphy', 'email': 'candidate018@example.com', 'edu': 'BA Design', 'exp': 5, 'role': 'UI/UX Designer', 'skills': 'Figma, Sketch', 'status': 'Available', 'loc': 'London'},
            {'code': 'CAN-019', 'first': 'Blake', 'last': 'Foster', 'email': 'candidate019@example.com', 'edu': 'MSc Data Science', 'exp': 3, 'role': 'Data Scientist', 'skills': 'Machine Learning, R, Python', 'status': 'Available', 'loc': 'San Francisco'},
            {'code': 'CAN-020', 'first': 'Ashley', 'last': 'Turner', 'email': 'candidate020@example.com', 'edu': 'BBA', 'exp': 1, 'role': 'Sales Representative', 'skills': 'Salesforce, Cold Calling', 'status': 'Available', 'loc': 'Chicago'}
        ]
        
        candidate_role = Role.query.filter_by(name='Candidate').first()
        
        for fc in fictional_candidates:
            # Add user if not exists
            user = User.query.filter_by(email=fc['email']).first()
            if not user:
                user = User(
                    first_name=fc['first'],
                    last_name=fc['last'],
                    email=fc['email'],
                    role_id=candidate_role.id
                )
                user.set_password('demo-password')
                db.session.add(user)
                db.session.commit()
                
            # Add candidate
            candidate = Candidate.query.filter_by(email=fc['email']).first()
            if not candidate:
                candidate = Candidate(
                    candidate_code=fc['code'],
                    first_name=fc['first'],
                    last_name=fc['last'],
                    email=fc['email'],
                    education=fc['edu'],
                    experience_years=fc['exp'],
                    current_role=fc['role'],
                    skills=fc['skills'],
                    location=fc['loc'],
                    status=fc['status'],
                    user_id=user.id
                )
                db.session.add(candidate)
        db.session.commit()
        print("Fictional candidates seeded.")

        # 9. Create fictional applications
        from app.models.application import Application
        import random

        # Fetch all open jobs
        open_jobs = Job.query.filter_by(status='Open').all()
        # Fetch all available candidates
        available_candidates = Candidate.query.filter_by(status='Available').all()

        statuses = ['Submitted', 'Under Review', 'Shortlisted', 'Rejected']
        existing_apps_count = Application.query.count()
        app_count = existing_apps_count

        if open_jobs and available_candidates:
            # We want around 30 applications
            for i in range(30):
                job = random.choice(open_jobs)
                candidate = random.choice(available_candidates)

                # Check for duplicates
                existing = Application.query.filter_by(candidate_id=candidate.id, job_id=job.id).first()
                if not existing:
                    app_count += 1
                    status = random.choice(statuses)
                    app_record = Application(
                        application_code=f"APP-{app_count:04d}",
                        candidate_id=candidate.id,
                        job_id=job.id,
                        cover_letter=f"Dear Hiring Manager,\n\nI am very interested in the {job.title} role. I believe my background fits your requirements well. Please find my profile attached.\n\nBest,\n{candidate.first_name} {candidate.last_name}",
                        status=status,
                        recruiter_notes="Candidate looks promising." if status in ['Under Review', 'Shortlisted'] else None
                    )
                    db.session.add(app_record)
            
            db.session.commit()
            print(f"{app_count} Fictional applications seeded.")

        # 10. Create Demo Skills
        from app.models.skill import Skill
        demo_skills = [
            {'name': 'Python', 'category': 'Programming', 'desc': 'High-level programming language for general-purpose programming.'},
            {'name': 'Java', 'category': 'Programming', 'desc': 'Class-based, object-oriented programming language.'},
            {'name': 'JavaScript', 'category': 'Web Development', 'desc': 'Lightweight interpreted programming language for web pages.'},
            {'name': 'React', 'category': 'Web Development', 'desc': 'Front-end JavaScript library for building user interfaces.'},
            {'name': 'Node.js', 'category': 'Web Development', 'desc': 'JavaScript runtime built on Chrome\'s V8 JavaScript engine.'},
            {'name': 'Flask', 'category': 'Web Development', 'desc': 'Micro web framework written in Python.'},
            {'name': 'Django', 'category': 'Web Development', 'desc': 'High-level Python web framework.'},
            {'name': 'SQL', 'category': 'Database', 'desc': 'Structured Query Language for managing data in relational databases.'},
            {'name': 'MySQL', 'category': 'Database', 'desc': 'Open-source relational database management system.'},
            {'name': 'PostgreSQL', 'category': 'Database', 'desc': 'Object-relational database system.'},
            {'name': 'MongoDB', 'category': 'Database', 'desc': 'Source-available cross-platform document-oriented database.'},
            {'name': 'HTML', 'category': 'Web Development', 'desc': 'Standard markup language for documents designed to be displayed in a web browser.'},
            {'name': 'CSS', 'category': 'Web Development', 'desc': 'Style sheet language used for describing the presentation of a document.'},
            {'name': 'Git', 'category': 'Tools', 'desc': 'Distributed version control system.'},
            {'name': 'Linux', 'category': 'Tools', 'desc': 'Open-source Unix-like operating system.'},
            {'name': 'Docker', 'category': 'DevOps', 'desc': 'Set of platform as a service products using OS-level virtualization.'},
            {'name': 'AWS', 'category': 'Cloud', 'desc': 'Amazon Web Services cloud computing platform.'},
            {'name': 'Azure', 'category': 'Cloud', 'desc': 'Microsoft Azure cloud computing platform.'},
            {'name': 'Cybersecurity', 'category': 'Cybersecurity', 'desc': 'Protection of computer systems and networks from information disclosure.'},
            {'name': 'Networking', 'category': 'Cybersecurity', 'desc': 'Computer networking and security protocols.'},
            {'name': 'Nmap', 'category': 'Cybersecurity', 'desc': 'Network scanner for network discovery and vulnerability auditing.'},
            {'name': 'Wireshark', 'category': 'Cybersecurity', 'desc': 'Free and open-source packet analyzer.'},
            {'name': 'Burp Suite', 'category': 'Cybersecurity', 'desc': 'Penetration testing and web vulnerability scanner tool.'},
            {'name': 'Machine Learning', 'category': 'Data', 'desc': 'Study of computer algorithms that improve automatically through experience.'},
            {'name': 'Data Analysis', 'category': 'Data', 'desc': 'Process of inspecting, cleansing, transforming, and modeling data.'}
        ]

        for s_data in demo_skills:
            skill = Skill.query.filter_by(name=s_data['name']).first()
            if not skill:
                skill = Skill(name=s_data['name'], category=s_data['category'], description=s_data['desc'])
                db.session.add(skill)
        db.session.commit()
        print("Demo skills seeded.")

        # 11. Create Demo Resumes
        import os
        from app.models.resume import Resume
        from app.services.skill_extractor import SkillExtractor

        upload_dir = app.config.get('UPLOAD_FOLDER')
        os.makedirs(upload_dir, exist_ok=True)

        candidates = Candidate.query.all()
        resumes_created = 0

        # Sample synthetic resume templates
        resume_templates = [
            ("Alex Demo", "Senior Python & Full-Stack Developer with 5+ years experience building web applications using Python, Flask, React, SQL, and Docker. Strong background in Git, Linux, and Cloud (AWS)."),
            ("Jordan Smith", "Backend Engineer specializing in Java, Node.js, PostgreSQL, MongoDB, and Docker. Experience with microservices, AWS, and Linux environment."),
            ("Taylor Wilson", "Data Analyst and Machine Learning enthusiast with expertise in Data Analysis, Python, SQL, PostgreSQL, and Data Visualizations."),
            ("Morgan Lee", "Cybersecurity Specialist skilled in Cybersecurity, Networking, Nmap, Wireshark, Burp Suite, and Linux system security."),
            ("Casey Patel", "Full Stack Developer proficient in JavaScript, React, HTML, CSS, Node.js, and MongoDB."),
            ("Sam Green", "DevOps Engineer focused on Docker, AWS, Azure, Linux, Git, and CI/CD automation pipelines."),
            ("Riley Davis", "Junior Software Developer with training in Python, Flask, SQL, Git, HTML, and CSS."),
            ("Jamie Chen", "Database Administrator with deep expertise in SQL, MySQL, PostgreSQL, and Database optimization."),
            ("Avery Clark", "Frontend Specialist focused on React, JavaScript, HTML, CSS, and UI component design."),
            ("Skyler White", "Software Engineer with knowledge of Java, Python, SQL, Docker, and AWS.")
        ]

        for idx, candidate in enumerate(candidates[:10]):
            existing_resume = Resume.query.filter_by(candidate_id=candidate.id).first()
            if not existing_resume:
                resumes_created += 1
                name, text_body = resume_templates[idx % len(resume_templates)]
                file_name = f"candidate{candidate.id:03d}_resume.txt"
                file_path = os.path.join(upload_dir, file_name)

                full_resume_text = f"Name: {candidate.first_name} {candidate.last_name}\nEmail: {candidate.email}\nPhone: {candidate.phone or '555-0199'}\n\nObjective:\nDriven professional seeking new opportunities.\n\nSummary:\n{text_body}\n\nEducation:\n{candidate.education or 'B.Tech Computer Science'}\n\nSkills:\n{candidate.skills or 'Python, SQL, Git'}"

                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(full_resume_text)

                file_size = os.path.getsize(file_path)
                extracted_skills = SkillExtractor.extract_skills(full_resume_text)

                resume = Resume(
                    resume_code=f"RES-{resumes_created:04d}",
                    candidate_id=candidate.id,
                    filename=file_name,
                    file_type='TXT',
                    file_size=file_size,
                    extracted_text=full_resume_text,
                    status='Parsed'
                )
                resume.set_skills_list(extracted_skills)
                db.session.add(resume)

        db.session.commit()
        print(f"{resumes_created} Demo resumes seeded.")

        # 12. Create Demo Interviews & Feedback
        from app.models.interview import Interview
        from app.models.interview_feedback import InterviewFeedback
        import random

        shortlisted_apps = Application.query.filter(Application.status.in_(['Shortlisted', 'Under Review'])).all()
        interviewer_names = ['Demo Interviewer', 'Sarah TechLead', 'David HRManager', 'Elena EngineeringMgr']
        interview_types = ['Technical', 'HR', 'Managerial', 'General']

        interviews_created = 0
        feedback_created = 0

        for idx, app_item in enumerate(shortlisted_apps[:12]):
            existing_int = Interview.query.filter_by(application_id=app_item.id).first()
            if not existing_int:
                interviews_created += 1
                int_code = f"INT-{interviews_created:04d}"
                date_str = f"2026-09-{(idx % 20) + 1:02d}"
                time_str = f"{(10 + (idx % 6)):02d}:00"
                itype = interview_types[idx % len(interview_types)]
                interviewer = interviewer_names[idx % len(interviewer_names)]

                interview = Interview(
                    interview_code=int_code,
                    application_id=app_item.id,
                    interviewer_name=interviewer,
                    interview_type=itype,
                    scheduled_date=date_str,
                    scheduled_time=time_str,
                    duration_minutes=45,
                    meeting_link="https://example.com/demo-interview",
                    status='Completed' if idx < 8 else 'Scheduled',
                    notes="Fictional candidate evaluation notes."
                )
                db.session.add(interview)
                db.session.commit()

                # Add Feedback for completed interviews
                if idx < 8:
                    feedback_created += 1
                    tech = random.randint(3, 5)
                    comm = random.randint(3, 5)
                    prob = random.randint(3, 5)
                    overall = round((tech + comm + prob) / 3.0, 2)
                    rec = 'Strongly Recommend' if overall >= 4.5 else ('Recommend' if overall >= 3.5 else 'Neutral')

                    fb = InterviewFeedback(
                        interview_id=interview.id,
                        technical_score=tech,
                        communication_score=comm,
                        problem_solving_score=prob,
                        overall_score=overall,
                        recommendation=rec,
                        comments="Candidate demonstrated clear domain knowledge and good problem solving skills."
                    )
                    db.session.add(fb)
                    db.session.commit()

        print(f"{interviews_created} Demo interviews and {feedback_created} feedback records seeded.")

        # 13. Create Demo Offers
        from app.models.offer import Offer

        all_apps = Application.query.all()
        offers_created = 0

        for idx, app_item in enumerate(all_apps[:6]):
            existing_off = Offer.query.filter_by(application_id=app_item.id).first()
            if not existing_off:
                offers_created += 1
                off_code = f"OFF-{offers_created:04d}"
                salary_options = ["$75,000 / year", "$85,000 / year", "$95,000 / year", "$110,000 / year"]
                sal = salary_options[idx % len(salary_options)]

                status_list = ['Draft', 'Sent', 'Accepted', 'Declined', 'Sent', 'Draft']
                off_status = status_list[idx % len(status_list)]

                offer = Offer(
                    offer_code=off_code,
                    application_id=app_item.id,
                    job_title=app_item.job.title if app_item.job else "Software Engineer",
                    employment_type="Full Time",
                    offered_salary=sal,
                    start_date="2026-10-01",
                    expiration_date="2026-10-15",
                    status=off_status,
                    notes="Fictional demo offer letter package."
                )
                db.session.add(offer)

                if off_status == 'Accepted':
                    app_item.status = 'Selected'

        db.session.commit()
        print(f"{offers_created} Demo offers seeded.")


        # Step 10: Attendance, Leave, Performance Seed Data
        from app.models.attendance import Attendance
        from app.models.leave_request import LeaveRequest
        from app.models.performance_review import PerformanceReview

        all_employees = Employee.query.all()

        # 14. Attendance Records (idempotent)
        att_dates = ["2026-08-01","2026-08-04","2026-08-05","2026-08-06","2026-08-07","2026-08-08"]
        statuses_c = ["Present","Present","Work From Home","Half Day","Present","Absent"]
        ci_times   = ["09:00:00","09:15:00","08:45:00","09:30:00","10:00:00",None]
        co_times   = ["18:00:00","17:45:00","18:15:00",None,"16:00:00",None]

        att_created = 0
        for emp in all_employees[:5]:
            for i, att_date in enumerate(att_dates):
                existing_att = Attendance.query.filter_by(employee_id=emp.id, attendance_date=att_date).first()
                if not existing_att:
                    status = statuses_c[i % len(statuses_c)]
                    ci = ci_times[i % len(ci_times)] if status != "Absent" else None
                    co = co_times[i % len(co_times)] if status not in ("Absent","Half Day") else None
                    wh = Attendance.calculate_work_hours(ci, co) if ci and co else None
                    att = Attendance(employee_id=emp.id, attendance_date=att_date, check_in=ci, check_out=co, status=status, work_hours=wh, remarks="Demo record")
                    db.session.add(att)
                    att_created += 1
        db.session.commit()
        print(str(att_created) + " Demo attendance records seeded.")

        # 15. Leave Requests (idempotent)
        leave_data = [
            {"ei":0,"type":"Casual","start":"2026-09-02","end":"2026-09-03","reason":"Personal errands","status":"Approved","comment":"Approved."},
            {"ei":1,"type":"Annual","start":"2026-09-10","end":"2026-09-17","reason":"Family vacation","status":"Approved","comment":"Approved."},
            {"ei":2,"type":"Personal","start":"2026-09-05","end":"2026-09-05","reason":"Personal matter","status":"Pending","comment":None},
            {"ei":3,"type":"Casual","start":"2026-08-30","end":"2026-08-30","reason":"Household work","status":"Rejected","comment":"Insufficient notice."},
            {"ei":4,"type":"Annual","start":"2026-10-01","end":"2026-10-10","reason":"Annual holiday","status":"Pending","comment":None},
            {"ei":0,"type":"Unpaid","start":"2026-09-20","end":"2026-09-21","reason":"Extended leave","status":"Pending","comment":None},
            {"ei":1,"type":"Casual","start":"2026-08-25","end":"2026-08-25","reason":"Personal reason","status":"Cancelled","comment":None},
            {"ei":2,"type":"Annual","start":"2026-11-01","end":"2026-11-07","reason":"Planned vacation","status":"Pending","comment":None},
            {"ei":3,"type":"Personal","start":"2026-10-15","end":"2026-10-16","reason":"Family commitment","status":"Approved","comment":"Approved."},
            {"ei":4,"type":"Casual","start":"2026-09-29","end":"2026-09-29","reason":"Sick day","status":"Pending","comment":None},
        ]
        leaves_created = 0
        for i, ld in enumerate(leave_data):
            if ld["ei"] >= len(all_employees): continue
            emp = all_employees[ld["ei"]]
            code = "LVE-" + str(i+1).zfill(4)
            if not LeaveRequest.query.filter_by(leave_code=code).first():
                lv = LeaveRequest(leave_code=code, employee_id=emp.id, leave_type=ld["type"], start_date=ld["start"], end_date=ld["end"], reason=ld["reason"], status=ld["status"], manager_comment=ld["comment"])
                db.session.add(lv)
                leaves_created += 1
        db.session.commit()
        print(str(leaves_created) + " Demo leave requests seeded.")

        # 16. Performance Reviews (idempotent)
        perf_data = [
            {"ei":0,"period":"Q1 2026","p":4,"q":5,"t":4,"g":5,"rev":"Morgan Davis","status":"Completed","c":"Excellent quarter."},
            {"ei":1,"period":"Q1 2026","p":3,"q":4,"t":5,"g":3,"rev":"Morgan Davis","status":"Completed","c":"Good team player."},
            {"ei":2,"period":"Q1 2026","p":5,"q":5,"t":4,"g":4,"rev":"Riley Chen","status":"Completed","c":"Outstanding performance."},
            {"ei":3,"period":"Q1 2026","p":4,"q":3,"t":4,"g":4,"rev":"Riley Chen","status":"Completed","c":"Good overall."},
            {"ei":4,"period":"Q1 2026","p":2,"q":3,"t":3,"g":2,"rev":"Morgan Davis","status":"Completed","c":"Needs improvement."},
            {"ei":0,"period":"Q2 2026","p":5,"q":5,"t":5,"g":4,"rev":"Morgan Davis","status":"Completed","c":"Exceptional Q2."},
            {"ei":1,"period":"Q2 2026","p":4,"q":4,"t":4,"g":4,"rev":"Morgan Davis","status":"Completed","c":"Consistent performance."},
            {"ei":2,"period":"Q2 2026","p":5,"q":4,"t":5,"g":5,"rev":"Riley Chen","status":"Draft","c":"Draft pending sign-off."},
            {"ei":3,"period":"Q2 2026","p":3,"q":4,"t":3,"g":3,"rev":"Riley Chen","status":"Draft","c":"Under review."},
            {"ei":4,"period":"Q2 2026","p":3,"q":3,"t":4,"g":3,"rev":"Morgan Davis","status":"Draft","c":"Showing improvement."},
        ]
        perf_created = 0
        for i, pd_item in enumerate(perf_data):
            if pd_item["ei"] >= len(all_employees): continue
            emp = all_employees[pd_item["ei"]]
            code = "PRV-" + str(i+1).zfill(4)
            if not PerformanceReview.query.filter_by(review_code=code).first():
                overall = PerformanceReview.compute_overall(pd_item["p"],pd_item["q"],pd_item["t"],pd_item["g"])
                pr = PerformanceReview(review_code=code, employee_id=emp.id, review_period=pd_item["period"], productivity_score=pd_item["p"], quality_score=pd_item["q"], teamwork_score=pd_item["t"], goal_score=pd_item["g"], overall_score=overall, reviewer_name=pd_item["rev"], comments=pd_item["c"], status=pd_item["status"])
                db.session.add(pr)
                perf_created += 1
        db.session.commit()
        print(str(perf_created) + " Demo performance reviews seeded.")

        # 17. Training Courses & Assignments
        from app.models.training import TrainingCourse, TrainingAssignment
        demo_courses = [
            {'code': 'TRN-0001', 'title': 'Data Privacy & Security Compliance', 'cat': 'Compliance', 'desc': 'Mandatory course on data protection best practices.', 'hours': 2, 'inst': 'Compliance Team'},
            {'code': 'TRN-0002', 'title': 'Advanced React Development', 'cat': 'Technical', 'desc': 'Modern hooks, state management, and web design.', 'hours': 8, 'inst': 'Tech Lead'},
            {'code': 'TRN-0003', 'title': 'Effective Workplace Communication', 'cat': 'Soft Skills', 'desc': 'Strategies for clear and constructive team collaboration.', 'hours': 4, 'inst': 'HR Specialist'},
            {'code': 'TRN-0004', 'title': 'Agile Project Management', 'cat': 'Management', 'desc': 'Scrum frameworks, sprint planning, and delivery.', 'hours': 6, 'inst': 'Agile Coach'}
        ]
        
        courses_created = 0
        for c in demo_courses:
            if not TrainingCourse.query.filter_by(course_code=c['code']).first():
                tc = TrainingCourse(course_code=c['code'], title=c['title'], category=c['cat'], description=c['desc'], duration_hours=c['hours'], instructor=c['inst'])
                db.session.add(tc)
                courses_created += 1
        db.session.commit()

        # Assign training to employees
        all_courses = TrainingCourse.query.all()
        assign_created = 0
        if all_courses and all_employees:
            for idx, emp in enumerate(all_employees[:6]):
                course = all_courses[idx % len(all_courses)]
                acode = f"TAS-{idx+1:04d}"
                if not TrainingAssignment.query.filter_by(assignment_code=acode).first():
                    ta = TrainingAssignment(
                        assignment_code=acode,
                        course_id=course.id,
                        employee_id=emp.id,
                        status='Completed' if idx < 3 else 'Assigned',
                        assigned_date='2026-08-01',
                        due_date='2026-09-15',
                        completion_date='2026-08-15' if idx < 3 else None,
                        score=95.0 if idx < 3 else None
                    )
                    db.session.add(ta)
                    assign_created += 1
        db.session.commit()

        # 18. Demo Notifications
        from app.models.notification import Notification
        all_users = User.query.all()
        notifs_created = 0
        for u in all_users:
            if Notification.query.filter_by(user_id=u.id).count() == 0:
                Notification.create_notification(
                    user_id=u.id,
                    title='Welcome to AI HR Platform',
                    message=f'Welcome {u.first_name}! Your account is active.',
                    link='/',
                    type='success'
                )
                Notification.create_notification(
                    user_id=u.id,
                    title='System Update',
                    message='Quarterly performance and training workflows are now open.',
                    link='/notifications',
                    type='info'
                )
                notifs_created += 2

        print(f"{courses_created} Training courses, {assign_created} assignments, and {notifs_created} notifications seeded.")
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
