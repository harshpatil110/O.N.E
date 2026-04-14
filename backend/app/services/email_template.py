def generate_completion_email_html(user, session, checklist, confidence_score, duration_hours) -> str:
    """
    Generate an HTML email report for HR after onboarding completion.
    Uses Warm Editorial Minimalism design (inline CSS only).
    """
    
    persona = session.persona or {}
    team = persona.get('team', 'N/A')
    
    tech_stack = persona.get('tech_stack', [])
    if isinstance(tech_stack, list):
        tech_stack_str = ", ".join(tech_stack) if tech_stack else 'N/A'
    else:
        tech_stack_str = str(tech_stack)
        
    start_date = user.created_at.strftime("%B %d, %Y") if user.created_at else 'Unknown'
    
    completed_items = [item for item in checklist if item.status == 'completed']
    pending_items = [item for item in checklist if item.status != 'completed']

    completed_html = "".join([
        f"<li style='margin-bottom: 8px; padding-left: 5px;'>{item.title}</li>" 
        for item in completed_items
    ])
    
    pending_html = ""
    if pending_items:
        pending_items_html = "".join([
            f"<li style='margin-bottom: 8px; padding-left: 5px;'>{item.title} <span style='font-size: 0.9em; opacity: 0.7;'>({item.status})</span></li>" 
            for item in pending_items
        ])
        str_pending = f"""
        <div style='margin-top: 30px;'>
            <h3 style='color: #8c8c8c; border-bottom: 1px solid #e0dfdc; padding-bottom: 8px; font-weight: 500;'>⚠️ Pending / Skipped Items</h3>
            <ul style='color: #8c8c8c; line-height: 1.6; padding-left: 20px;'>
                {pending_items_html}
            </ul>
        </div>
        """
        pending_html = str_pending

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="margin: 0; padding: 40px; background-color: #F7F5F0; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333333;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #FFFFFF; padding: 40px; border: 1px solid #EAE8E2; border-radius: 4px;">
            
            <h2 style="margin-top: 0; font-weight: 600; color: #1a1a1a; letter-spacing: -0.5px;">
                ✅ Onboarding Completed — {user.name} ({user.role})
            </h2>
            
            <p style="color: #666; font-size: 15px; margin-bottom: 30px;">
                The automated onboarding sequence has been completed successfully. 
                Below is the summary report.
            </p>

            <table style="width: 100%; border-collapse: collapse; margin-bottom: 30px; font-size: 14px;">
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; width: 120px; color: #666;">Name</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{user.name}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; color: #666;">Email</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{user.email}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; color: #666;">Role</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{user.role}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; color: #666;">Team</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{team}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; color: #666;">Tech Stack</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{tech_stack_str}</td>
                </tr>
                <tr>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; color: #666;">Start Date</td>
                    <td style="padding: 12px 0; border-bottom: 1px solid #EAE8E2; font-weight: 500;">{start_date}</td>
                </tr>
            </table>

            <div style="background-color: #FAFAFA; padding: 20px; border: 1px solid #EAE8E2; margin-bottom: 30px; border-radius: 4px;">
                <table style="width: 100%; text-align: center;">
                    <tr>
                        <td style="width: 50%; border-right: 1px solid #EAE8E2;">
                            <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Confidence Score</div>
                            <div style="font-size: 24px; font-weight: 600; color: #000;">{confidence_score}%</div>
                        </td>
                        <td style="width: 50%;">
                            <div style="font-size: 12px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Total Duration</div>
                            <div style="font-size: 24px; font-weight: 600; color: #000;">{duration_hours:.1f} hours</div>
                        </td>
                    </tr>
                </table>
            </div>

            <div>
                <h3 style="color: #1a1a1a; border-bottom: 1px solid #EAE8E2; padding-bottom: 8px; font-weight: 500;">✅ Completed Items</h3>
                <ol style="color: #333; line-height: 1.6; padding-left: 20px; font-size: 14px;">
                    {completed_html}
                </ol>
            </div>

            {pending_html}

            <div style="margin-top: 50px; font-size: 12px; color: #999; text-align: center; border-top: 1px solid #EAE8E2; padding-top: 20px;">
                This is an automated notification from O.N.E
                <br>Session ID: {session.id}
            </div>

        </div>
    </body>
    </html>
    """
    
    return html_content
