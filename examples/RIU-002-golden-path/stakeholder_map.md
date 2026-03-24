# Stakeholder Map — AI Customer Service Assistant

## Scenario Context

A mid-size insurance company wants to add an AI assistant for customer service. Three stakeholders have different priorities: CTO (cost reduction), VP of Customer Service (CSAT improvement), CEO (market positioning / press release). This stakeholder map was built after a compliance VP blocked a similar project at a peer company — we're doing this proactively.

## Stakeholder Registry

| # | Stakeholder | Title | Decision Authority | Influence Level | Interest Level | Discovery Method |
|---|-------------|-------|--------------------|-----------------|----------------|------------------|
| 1 | Sarah Chen | CTO | Technical architecture, vendor selection, infrastructure budget | High | High | Sponsor — named in kickoff |
| 2 | Marcus Rivera | VP Customer Service | CS workflow changes, agent training, CSAT targets | High | High | Sponsor — named in kickoff |
| 3 | Diana Park | CEO | Final GO/NO-GO on public launch, press release approval | Critical | Medium | Sponsor — named in kickoff |
| 4 | Raj Patel | VP Compliance | Data handling policy, PII rules, regulatory sign-off | Critical (veto) | Medium | **Discovered via checklist** — regulatory authority over customer data |
| 5 | Lisa Yamamoto | CISO | Security review, pen testing, data residency | Critical (veto) | Low | **Discovered via checklist** — any system touching customer PII |
| 6 | Tom Bradley | Head of Legal | Contract review for AI vendor, liability for AI responses | High (veto on legal) | Low | **Discovered via checklist** — vendor contracts + AI liability |
| 7 | Ana Ruiz | CS Team Lead (Tier 1) | Daily workflow impact, escalation handling | Medium | High | Identified as end-user representative |
| 8 | James Ko | Data Engineering Lead | Data pipeline, integration with CRM, model serving | Medium | High | Technical dependency — owns the data platform |
| 9 | Priya Sharma | Customer Experience Director | Brand voice, tone guidelines, customer communication standards | Medium | Medium | **Discovered via checklist** — any customer-facing communication |
| 10 | Finance (CFO office) | Budget Approval | Budget above $200K requires CFO sign-off | High (conditional) | Low | **Discovered via checklist** — procurement threshold |

## Hidden Stakeholders — Discovery Process

Used the **Stakeholder Discovery Checklist** (systematic sweep of 6 categories):

| Category | Question | Stakeholder Found |
|----------|----------|-------------------|
| Regulatory | Who has authority over data used by this system? | Raj Patel (VP Compliance) |
| Security | Who must approve systems that access customer PII? | Lisa Yamamoto (CISO) |
| Legal | Who reviews vendor contracts and liability exposure? | Tom Bradley (Head of Legal) |
| Brand/CX | Who owns the customer communication standards? | Priya Sharma (CX Director) |
| Budget | Who approves expenditures at the expected project scale? | CFO Office (conditional) |
| End Users | Who will the system change daily work for? | Ana Ruiz (CS Team Lead) |

**Key insight**: Stakeholders 4-6 (Compliance, CISO, Legal) have **veto power** but were not in the original kickoff. In the peer company incident, Compliance blocked deployment 3 weeks in. By surfacing them now, we avoid that failure mode entirely.

## Influence-Interest Matrix

```
                    Low Interest          Medium Interest       High Interest
                ┌─────────────────┬─────────────────────┬──────────────────┐
Critical        │  Lisa (CISO)    │  Diana (CEO)        │                  │
Authority       │                 │  Raj (Compliance)   │                  │
                ├─────────────────┼─────────────────────┼──────────────────┤
High            │  Tom (Legal)    │  Priya (CX Dir)     │  Sarah (CTO)     │
Authority       │  Finance (CFO)  │                     │  Marcus (VP CS)  │
                ├─────────────────┼─────────────────────┼──────────────────┤
Medium          │                 │                     │  Ana (CS Lead)   │
Authority       │                 │                     │  James (Data Eng)|
                └─────────────────┴─────────────────────┴──────────────────┘
```

**Engagement strategy by quadrant**:
- Critical + Low/Medium interest: **Keep satisfied** — brief monthly, escalate only when their domain is affected. Schedule dedicated review gates.
- High + High interest: **Manage closely** — weekly standups, decision authority on their domains.
- Medium + High interest: **Keep informed** — biweekly updates, input on design but not decision authority.

## References

- Stakeholder Discovery Checklist adapted from PMI stakeholder analysis framework (https://www.pmi.org/learning/library/stakeholder-analysis-pivotal-practice-projects-8905)
- Influence-Interest matrix based on Mendelow's Power/Interest Grid (source: Eden, C. & Ackermann, F., "Making Strategy", 1998)
- Hidden stakeholder identification pattern from Palette Knowledge Library LIB-001, LIB-007
