from textwrap import dedent
from typing import List, Tuple

from .registry import ComponentRegistry


@ComponentRegistry.register("multi-step-wizard")
def forge_multi_step_wizard(name: str, props: List[Tuple[str, str]]) -> str:
    # This artisan forges a stateful, multi-step form or onboarding flow.
    return dedent(r'''
'use client';

import React, { useState, FormEvent, ReactElement } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { cn } from '@/lib/utils';

// The Gnostic Hook for managing wizard state
function useMultiStepForm(steps: ReactElement[]) {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);

  function next() {
    setCurrentStepIndex(i => {
      if (i >= steps.length - 1) return i;
      return i + 1;
    });
  }

  function back() {
    setCurrentStepIndex(i => {
      if (i <= 0) return i;
      return i - 1;
    });
  }

  function goTo(index: number) {
    setCurrentStepIndex(index);
  }

  return {
    currentStepIndex,
    step: steps[currentStepIndex],
    steps,
    isFirstStep: currentStepIndex === 0,
    isLastStep: currentStepIndex === steps.length - 1,
    goTo,
    next,
    back,
  };
}

// Dummy Step Components (To be replaced by the Architect's will)
const Step1 = () => <div>Step 1: Welcome</div>;
const Step2 = () => <div>Step 2: Configuration</div>;
const Step3 = () => <div>Step 3: Finalization</div>;

export function MultiStepWizard({ className }: { className?: string }) {
  const { steps, currentStepIndex, step, isFirstStep, isLastStep, back, next } = useMultiStepForm([
    <Step1 />,
    <Step2 />,
    <Step3 />,
  ]);

  function onSubmit(e: FormEvent) {
    e.preventDefault();
    if (!isLastStep) return next();
    alert("Onboarding Complete!");
  }

  return (
    <Card className={cn("w-[450px]", className)}>
      <form onSubmit={onSubmit}>
        <CardHeader>
          <CardTitle>
            Onboarding ({currentStepIndex + 1} / {steps.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          {step}
        </CardContent>
        <CardFooter className="flex justify-between">
          {!isFirstStep && (
            <Button type="button" variant="ghost" onClick={back}>
              Back
            </Button>
          )}
          <Button type="submit" className={isFirstStep ? "ml-auto" : ""}>
            {isLastStep ? "Finish" : "Next"}
          </Button>
        </CardFooter>
      </form>
    </Card>
  );
}
''')