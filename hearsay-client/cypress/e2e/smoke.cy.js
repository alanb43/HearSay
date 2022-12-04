/// <reference types="cypress" />

it('does not smoke', () => {
  cy.visit('localhost:3000');

  cy.get('#submit-button')
    .should('be.visible');
  
  cy.get('#search-bar')
    .type('Is Lebron getting traded to the Detroit Pistons?')
    .should('be.visible')
    .should('have.value', 'Is Lebron getting traded to the Detroit Pistons?');
  
  cy.get('button')
    .eq(1)
    .should('be.visible');
  
  cy.get('#submit-button')
    .click();
  
  cy.get('.HearSay')
    .eq(0)
    .should('be.visible');
});
