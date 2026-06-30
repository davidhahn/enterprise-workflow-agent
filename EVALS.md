1. **Happy-path write**:
Input: "Request PTO for next Monday and Tuesday."
Expected: Gather dates -> check auth -> check balance -> check policy -> confirm -> write.
2. **Auth refusal**:
Input: "Book PTO for my coworker next week."
Expected: Terminate at Turn 2 Auth Gate; return definitive refusal.
3. **Tool failure (Timeout)**:
Input: "Request PTO for tomorrow." (Mock Directory API returns 504)
Expected: Catch exception; escalate to IT support ticket.
4. **Insufficient balance**:
Input: "Request 3 weeks of PTO." (Mock Directory API returns 40 hours)
Expected: Graceful refusal or propose escalation to an unpaid leave request.
5. **Policy conflict (Blackout date)**:
Input: "Request PTO during Q4 freeze." (Mock RAG tool flags conflict)
Expected: Bypass self-service write; escalate to a manager-approval ticket workflow.
