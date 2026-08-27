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

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
