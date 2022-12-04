/// <reference types="cypress" />

describe('HearSay q&a functional test', () => {
  it('tests the injured intent', () => {
    cy.visit('localhost:3000');
  
    // testing injury intent
    cy.get('#search-bar')
      .type('Are any of the LA Lakers injured?')
      .should('have.value', 'Are any of the LA Lakers injured?');
    
    cy.get('#submit-button')
      .click();
    
    cy.wait(8000); 
    // response generation: sentiment
    cy.get('.HearSay')
      .eq(0)
      .contains('The overall sentiment is');
  });
  
  it('tests the question and answering intent', () => {
    // testing intent-less question + answering
    cy.get('#search-bar')
      .type('Is Lionel Messi the greatest soccer player ever?');
    
    cy.get('#submit-button')
      .click();
    
    cy.wait(8000);
    // response generation: short answer 
    cy.get('.HearSay')
      .eq(1)
      .contains('The short answer is');
  });

  it('tests the trade intent', () => {
    // testing intent-less question + answering
    cy.get('#search-bar')
      .type('Should LeBron get traded to the Detroit Pistons?');
    
    cy.get('#submit-button')
      .click();
    
    cy.wait(10000);
    // response generation: short answer 
    cy.get('.HearSay')
      .eq(2)
      .contains('The most relevant tweet is');
  });
});
