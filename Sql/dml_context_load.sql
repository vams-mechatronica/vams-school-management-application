------ Staff Categories --------
INSERT INTO staffs_staffcategory (name) VALUES
	 ('Teaching Staff'),
	 ('Non-Technical Staff'),
	 ('Technical Staff'),
	 ('Cleaning Staff');


------ Student Class ----------
INSERT INTO corecode_studentclass (name,tuition_fees,computer_fees,admission_fees,exam_fees,miscellaneous) VALUES
	 ('XI',200.00,0.00,0.00,0.00,0.00),
	 ('XII',2000.00,200.00,10000.00,300.00,0.00),
	 ('Pre-Nursery',0.00,0.00,0.00,0.00,0.00),
	 ('III',0.00,0.00,0.00,0.00,0.00),
	 ('I',0.00,0.00,0.00,0.00,0.00),
	 ('II',0.00,0.00,0.00,0.00,0.00),
	 ('IV',0.00,0.00,0.00,0.00,0.00),
	 ('V',0.00,0.00,0.00,0.00,0.00),
	 ('VI',0.00,0.00,0.00,0.00,0.00),
	 ('VII',0.00,0.00,0.00,0.00,0.00);
INSERT INTO corecode_studentclass (name,tuition_fees,computer_fees,admission_fees,exam_fees,miscellaneous) VALUES
	 ('VIII',0.00,0.00,0.00,0.00,0.00),
	 ('IX',0.00,0.00,0.00,0.00,0.00),
	 ('X',0.00,0.00,0.00,0.00,0.00),
	 ('UKG',0.00,0.00,0.00,0.00,0.00),
	 ('Nursery',0.00,0.00,0.00,0.00,0.00),
	 ('LKG',0.00,0.00,0.00,0.00,0.00);


-------Subjects--------------
INSERT INTO corecode_subject (name,test_max_marks,exam_max_marks) VALUES
	 ('Punjabi',50,100);







-------Email template ---------

INSERT INTO vams_sms.email_module_emailtemplate (name,subject,body,is_active,created_at,updated_at) VALUES
	 ('new_student_enrollment_congratulation','Congratulations! You are now enrolled to __schoolname__','<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {
      font-family: ''Segoe UI'', Tahoma, Geneva, Verdana, sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
    }
    .container {
      max-width: 600px;
      background-color: #ffffff;
      margin: 40px auto;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .header {
      text-align: center;
      border-bottom: 1px solid #e0e0e0;
      padding-bottom: 15px;
      margin-bottom: 25px;
    }
    .header h1 {
      color: #2e86de;
      font-size: 24px;
      margin: 0;
    }
    .content p {
      font-size: 16px;
      color: #333333;
      line-height: 1.6;
    }
    .highlight-box {
      background-color: #f0f8ff;
      padding: 15px;
      border-left: 5px solid #2e86de;
      margin: 20px 0;
      border-radius: 4px;
    }
    .highlight-box strong {
      display: block;
      margin-bottom: 8px;
      color: #000;
    }
    .credentials {
      background-color: #fff6e5;
      padding: 15px;
      border-left: 5px solid #f39c12;
      margin: 20px 0;
      border-radius: 4px;
      font-family: monospace;
    }
    .footer {
      text-align: center;
      font-size: 13px;
      color: #999999;
      margin-top: 30px;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Welcome to {{ sitename }}</h1>
    </div>
    <div class="content">
      <p>Dear {{ student_name }},</p>
      <p>
        Congratulations! We are excited to confirm your admission to <strong>{{ sitename }}</strong>.
      </p>

      <div class="highlight-box">
        <strong>Admission Details:</strong>
        Registration Number: <strong>{{ registration_number }}</strong><br>
        Assigned Class: <strong>{{ class_name }}</strong>
      </div>

      <p>Below are your login credentials to access the student portal:</p>

      <div class="credentials">
        <strong>Portal Login:</strong><br>
        Username: {{ username }}<br>
        Password: {{ password }}
      </div>

      <p>
        For security, please log in and change your password after your first login.
      </p>

      <p>
        If you need assistance, feel free to contact our support team.
      </p>

      <p>Warm regards,</p>
      <p><strong>{{ sitename }} Admissions Team</strong></p>
    </div>
    <div class="footer">
      &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
  </div>
</body>
</html>',1,'2025-05-12 02:56:45.683750','2025-05-12 03:15:50.837876'),
	 ('new_staff_enrollment_congratulation','Congratulations! You are now enrolled to __schoolname__','<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Welcome to {{ sitename }}</title>
    <style>
        body {
            font-family: "Segoe UI", sans-serif;
            background-color: #f5f6fa;
            color: #333;
            padding: 0;
            margin: 0;
        }
        .container {
            width: 90%;
            max-width: 600px;
            background-color: #fff;
            margin: 40px auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        .header {
            background-color: #2c3e50;
            color: #ffffff;
            padding: 24px 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 22px;
        }
        .content {
            padding: 30px;
        }
        .content h2 {
            color: #2c3e50;
        }
        .details-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .details-table td {
            padding: 10px;
            border-bottom: 1px solid #eee;
        }
        .details-table td:first-child {
            font-weight: 600;
            color: #555;
        }
        .footer {
            background-color: #ecf0f1;
            text-align: center;
            padding: 18px 30px;
            font-size: 14px;
            color: #666;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>Welcome to {{ sitename }}</h1>
    </div>
    <div class="content">
        <h2>Hello {{ full_name }},</h2>
        <p>We are excited to inform you that you have been successfully enrolled as a staff member at <strong>{{ sitename }}</strong>.</p>

        <table class="details-table">
            <tr>
                <td>Full Name:</td>
                <td>{{ full_name }}</td>
            </tr>
            <tr>
                <td>Department:</td>
                <td>{{ department }}</td>
            </tr>
            <tr>
                <td>Designation:</td>
                <td>{{ designation }}</td>
            </tr>
            <tr>
                <td>Email Address:</td>
                <td>{{ email }}</td>
            </tr>
            <tr>
                <td>Username:</td>
                <td>{{ username }}</td>
            </tr>
            <tr>
                <td>Temporary Password:</td>
                <td>{{ password }}</td>
            </tr>
        </table>

        <p style="margin-top: 20px;">You can now log in to the staff portal using the above credentials. Please change your password after your first login.</p>
        <p>We look forward to your valuable contribution.</p>

        <p>Best regards,<br>{{ sitename }} Admin Team</p>
    </div>
    <div class="footer">
        &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
</div>
</body>
</html>',1,'2025-05-12 11:02:43.336845','2025-05-12 11:02:43.336876'),
	 ('new_leave_request','Urgent! __staffname__ requested for leave please review','<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>New Leave Request</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
      color: #333;
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .header {
      background-color: #007bff;
      color: white;
      padding: 20px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 20px;
    }
    .content {
      padding: 30px;
    }
    .content p {
      font-size: 16px;
      margin-bottom: 20px;
    }
    .details-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }
    .details-table td {
      padding: 10px;
      border-bottom: 1px solid #eaeaea;
    }
    .details-table td:first-child {
      font-weight: 600;
      width: 150px;
      color: #555;
    }
    .actions {
      margin-top: 30px;
      text-align: center;
    }
    .btn {
      display: inline-block;
      padding: 10px 20px;
      margin: 0 10px;
      text-decoration: none;
      color: white;
      border-radius: 5px;
      font-weight: bold;
    }
    .btn-approve {
      background-color: #28a745;
    }
    .btn-reject {
      background-color: #dc3545;
    }
    .footer {
      background-color: #f0f0f0;
      padding: 16px 30px;
      text-align: center;
      font-size: 14px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>New Leave Request Submitted</h1>
    </div>
    <div class="content">
      <p>Dear {{ approver_name }},</p>
      <p><strong>{{ staff_name }}</strong> has submitted a leave request. Below are the details:</p>

      <table class="details-table">
        <tr>
          <td>Staff Name:</td>
          <td>{{ staff_name }}</td>
        </tr>
        <tr>
          <td>Email:</td>
          <td>{{ staff_email }}</td>
        </tr>
        <tr>
          <td>Leave Type:</td>
          <td>{{ leave_type }}</td>
        </tr>
        <tr>
          <td>Start Date:</td>
          <td>{{ start_date }}</td>
        </tr>
        <tr>
          <td>End Date:</td>
          <td>{{ end_date }}</td>
        </tr>
        <tr>
          <td>Reason:</td>
          <td>{{ reason }}</td>
        </tr>
      </table>

      <div class="actions">
        <a href="{{ approve_url }}" class="btn btn-approve">Approve</a>
        <a href="{{ reject_url }}" class="btn btn-reject">Reject</a>
      </div>

      <p style="margin-top: 20px;">Please click a button above to respond to the request.</p>
      <p>Regards,<br>{{ sitename }} Automated Notification</p>
    </div>
    <div class="footer">
      &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
  </div>
</body>
</html>',1,'2025-05-12 11:06:00.275518','2025-05-12 11:06:00.275549'),
	 ('leave_request_submitted','Your leave request has been submitted successfully','<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Leave Request Submitted</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
      color: #333;
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .header {
      background-color: #17a2b8;
      color: white;
      padding: 20px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 20px;
    }
    .content {
      padding: 30px;
    }
    .content p {
      font-size: 16px;
      margin-bottom: 20px;
    }
    .details-table {
      width: 100%;
      border-collapse: collapse;
    }
    .details-table td {
      padding: 10px;
      border-bottom: 1px solid #eaeaea;
    }
    .details-table td:first-child {
      font-weight: 600;
      width: 150px;
      color: #555;
    }
    .footer {
      background-color: #f0f0f0;
      padding: 16px 30px;
      text-align: center;
      font-size: 14px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Leave Request Submitted</h1>
    </div>
    <div class="content">
      <p>Dear {{ staff_name }},</p>
      <p>Your leave request has been successfully submitted. Below are the details:</p>

      <table class="details-table">
        <tr>
          <td>Leave Type:</td>
          <td>{{ leave_type }}</td>
        </tr>
        <tr>
          <td>Start Date:</td>
          <td>{{ start_date }}</td>
        </tr>
        <tr>
          <td>End Date:</td>
          <td>{{ end_date }}</td>
        </tr>
        <tr>
          <td>Reason:</td>
          <td>{{ reason }}</td>
        </tr>
        <tr>
          <td>Status:</td>
          <td><strong style="color: #ffc107;">Pending Approval</strong></td>
        </tr>
      </table>

      <p style="margin-top: 20px;">You will receive an update once your request has been reviewed.</p>
      <p>Regards,<br>{{ sitename }} HR Team</p>
    </div>
    <div class="footer">
      &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
  </div>
</body>
</html>',1,'2025-05-12 11:07:22.522825','2025-05-12 11:07:22.522857'),
	 ('leave_request_approved','Congratulations! Your leave request has been approved','<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Leave Approved</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
      color: #333;
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .header {
      background-color: #28a745;
      color: white;
      padding: 20px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 20px;
    }
    .content {
      padding: 30px;
    }
    .content p {
      font-size: 16px;
      margin-bottom: 20px;
    }
    .details-table {
      width: 100%;
      border-collapse: collapse;
    }
    .details-table td {
      padding: 10px;
      border-bottom: 1px solid #eaeaea;
    }
    .details-table td:first-child {
      font-weight: 600;
      width: 150px;
      color: #555;
    }
    .footer {
      background-color: #f0f0f0;
      padding: 16px 30px;
      text-align: center;
      font-size: 14px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Leave Approved</h1>
    </div>
    <div class="content">
      <p>Dear {{ staff_name }},</p>
      <p>We are pleased to inform you that your leave request has been <strong style="color: #28a745;">approved</strong>. Below are the approved leave details:</p>

      <table class="details-table">
        <tr>
          <td>Leave Type:</td>
          <td>{{ leave_type }}</td>
        </tr>
        <tr>
          <td>Start Date:</td>
          <td>{{ start_date }}</td>
        </tr>
        <tr>
          <td>End Date:</td>
          <td>{{ end_date }}</td>
        </tr>
        <tr>
          <td>Reason:</td>
          <td>{{ reason }}</td>
        </tr>
        <tr>
          <td>Approved By:</td>
          <td>{{ approved_by }}</td>
        </tr>
      </table>

      <p style="margin-top: 20px;">Wishing you a restful and productive time away.</p>
      <p>Regards,<br>{{ sitename }} HR Team</p>
    </div>
    <div class="footer">
      &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
  </div>
</body>
</html>',1,'2025-05-12 11:08:48.395834','2025-05-12 11:08:48.395866'),
	 ('leave_request_rejected','Your leave request has been rejected','<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Leave Request Rejected</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background-color: #f4f6f9;
      margin: 0;
      padding: 0;
      color: #333;
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background: #fff;
      border-radius: 8px;
      overflow: hidden;
      box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    .header {
      background-color: #dc3545;
      color: white;
      padding: 20px 30px;
      text-align: center;
    }
    .header h1 {
      margin: 0;
      font-size: 20px;
    }
    .content {
      padding: 30px;
    }
    .content p {
      font-size: 16px;
      margin-bottom: 20px;
    }
    .details-table {
      width: 100%;
      border-collapse: collapse;
    }
    .details-table td {
      padding: 10px;
      border-bottom: 1px solid #eaeaea;
    }
    .details-table td:first-child {
      font-weight: 600;
      width: 150px;
      color: #555;
    }
    .footer {
      background-color: #f0f0f0;
      padding: 16px 30px;
      text-align: center;
      font-size: 14px;
      color: #777;
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>Leave Request Rejected</h1>
    </div>
    <div class="content">
      <p>Dear {{ staff_name }},</p>
      <p>We regret to inform you that your leave request has been <strong style="color: #dc3545;">rejected</strong>. Please find the details below:</p>

      <table class="details-table">
        <tr>
          <td>Leave Type:</td>
          <td>{{ leave_type }}</td>
        </tr>
        <tr>
          <td>Start Date:</td>
          <td>{{ start_date }}</td>
        </tr>
        <tr>
          <td>End Date:</td>
          <td>{{ end_date }}</td>
        </tr>
        <tr>
          <td>Reason:</td>
          <td>{{ reason }}</td>
        </tr>
        <tr>
          <td>Reviewed By:</td>
          <td>{{ reviewed_by }}</td>
        </tr>
        <tr>
          <td>Remarks:</td>
          <td>{{ remarks|default:"N/A" }}</td>
        </tr>
      </table>

      <p style="margin-top: 20px;">If you have any questions or concerns regarding this decision, please reach out to HR.</p>
      <p>Regards,<br>{{ sitename }} HR Team</p>
    </div>
    <div class="footer">
      &copy; {{ current_year }} {{ sitename }}. All rights reserved.
    </div>
  </div>
</body>
</html>',1,'2025-05-12 11:10:10.373312','2025-05-12 11:10:10.373356');


