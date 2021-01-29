# The donationbox frontend

The donationbox frontend:project uses :create-react-app.
:It /has an app:module and a donations:module.
The app:module /contains a global:store. :It has a :router.

## The donations:module

The donations:module /contains a donation:store, a donation:view and a thank-you:view.
The donation:store /stores the current donation:entity.
:It has a submit:resource-state.

### The donation:view

The donation:view /has a :route.
:It /has a donation:form that (/saves the donation:entity) and (/uses the submit:resource-state).

### The thank-you:view

The thank-you:view /has a :route.
