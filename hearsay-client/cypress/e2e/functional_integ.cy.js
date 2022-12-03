/// <reference types="cypress" />

describe('HearSay user profile setup functional test', () => {
  
  it('starts back-end profile creation using conversation', () => {  
    cy.visit('localhost:3000');
    
    cy.get('#search-bar')
      .type('I\'d like to create a profile')
      .should('have.value', 'I\'d like to create a profile');

    cy.get('#submit-button')
      .click();

    cy.wait(1000);
    cy.get('.HearSay')
      .should('have.text', 'What\'s your name?');
  });

  it('builds out user profile', () => {
    cy.get('#search-bar')
      .type('Alan');

    cy.get('#submit-button')
      .click();

    cy.wait(1500);
    cy.get('.HearSay').eq(1)
      .should('have.text', 'Nice to meet you, Alan. Which teams do you support?');
    
    cy.get('#search-bar')
      .type('Manchester United');

    cy.get('#submit-button')
      .click();
    
    cy.wait(1500);
    cy.get('.HearSay').eq(2)
      .should('have.text', 'Ah, a Manchester United fan I see. Have any favorite players?');

    cy.get('#search-bar')
      .type('LeBron James');

    cy.get('#submit-button')
      .click();
    
    cy.wait(1500);
    cy.get('.HearSay').eq(3)
      .should('have.text', 'Got it. I\'ve set up your profile!');
  });
});
