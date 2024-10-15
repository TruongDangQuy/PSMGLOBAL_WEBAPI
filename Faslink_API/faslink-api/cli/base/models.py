from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, NVARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint
from ...database import Base

class BaseEmployee(Base):
    __tablename__ = "BaseEmployee"

    id = Column(Integer, primary_key=True, autoincrement = False)
    metatype = Column(String)
    code = Column(String)
    first_name = Column(NVARCHAR)
    last_name = Column(NVARCHAR)
    title = Column(NVARCHAR)
    is_primary = Column(String)
    user_id = Column(String)
    email = Column(String)
    gender = Column(String)
    phone = Column(String)
    dob_day = Column(Integer)
    dob_month = Column(Integer)
    dob_year= Column(Integer)
    tax_id   = Column(String)
    insurance_id  = Column(String)
    team_id   = Column(String)
    timesheet_id  = Column(String)
    office_id   = Column(String)
    employee_type_id  = Column(String)
    area_id   = Column(String)
    position_id  = Column(String)
    payroll_policy_id  = Column(String)
    is_terminated  = Column(String)
    terminated_date  = Column(Integer)
    start_date  = Column(Integer)
    official_start_date  = Column(Integer)
    last_update  = Column(Integer)
    name    = Column(NVARCHAR)
    type    = Column(String)
    extracted_at  = Column(DateTime)

class BaseTimeoff(Base):
    __tablename__ = "BaseTimeoff"

    id = Column(Integer, primary_key=True, autoincrement = False)
    type = Column(String)
    hid = Column(String)
    code = Column(String)
    name = Column(NVARCHAR)
    content = Column(NVARCHAR)
    cut_off = Column(NVARCHAR)
    user_id = Column(String)
    username = Column(String)
    creator_id = Column(String)
    creator_username = Column(String)
    status = Column(String)
    confirm = Column(String)
    metatype = Column(String)
    locked = Column(String)
    warning = Column(String)
    since = Column(Integer)
    last_update = Column(Integer)
    token = Column(String)
    workflow = Column(String)
    group_id = Column(String)
    state = Column(String)
    paid_timeoff = Column(Integer)
    deadline = Column(Integer)
    deadline_confirm = Column(Integer)
    start_date = Column(Integer)
    end_date = Column(Integer)
    extracted_at = Column(DateTime)

class BaseTeam(Base):
    __tablename__ = "BaseTeam"

    id = Column(Integer, primary_key=True, autoincrement = False)
    name = Column(NVARCHAR)
    code = Column(String)
    area_id = Column(String)
    dept_id = Column(String)
    content = Column(NVARCHAR)
    metatype = Column(NVARCHAR)
    creator_id = Column(String)
    since = Column(Integer)
    last_update = Column(Integer)
    extracted_at = Column(DateTime)

class BaseArea(Base):
    __tablename__ = "BaseArea"

    id = Column(Integer, primary_key=True, autoincrement = False)
    name = Column(NVARCHAR)
    code = Column(NVARCHAR)
    content = Column(NVARCHAR)
    metatype = Column(NVARCHAR)
    type = Column(NVARCHAR)
    since = Column(Integer)
    last_update = Column(Integer)
    extracted_at = Column(DateTime)


class API_TD(Base):
    __tablename__ = "API_TD"

    _id = Column(String(255), primary_key=True)
    staff_code = Column(String)
    gender = Column(String)
    email = Column(String)
    phone = Column(String)
    first_name = Column(NVARCHAR)
    last_name = Column(NVARCHAR)
    full_name = Column(NVARCHAR)
    