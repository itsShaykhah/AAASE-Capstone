import { useState, type FormEvent } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { CAMPAIGN_OBJECTIVES, type CampaignObjective, type CampaignRequest } from "@/lib/types";

interface CampaignFormProps {
  onSubmit: (request: CampaignRequest) => void;
  isSubmitting: boolean;
}

interface FormErrors {
  product_name?: string;
  product_description?: string;
}

const MIN_DESCRIPTION_LENGTH = 10;

export function CampaignForm({ onSubmit, isSubmitting }: CampaignFormProps) {
  const [productName, setProductName] = useState("");
  const [productDescription, setProductDescription] = useState("");
  const [objective, setObjective] = useState<CampaignObjective>("brand_awareness");
  const [targetAudience, setTargetAudience] = useState("");
  const [durationDays, setDurationDays] = useState("");
  const [brandTone, setBrandTone] = useState("");
  const [additionalNotes, setAdditionalNotes] = useState("");
  const [errors, setErrors] = useState<FormErrors>({});

  function validate(): boolean {
    const nextErrors: FormErrors = {};
    if (productName.trim().length < 2) {
      nextErrors.product_name = "Enter a product name (at least 2 characters).";
    }
    if (productDescription.trim().length < MIN_DESCRIPTION_LENGTH) {
      nextErrors.product_description = `Describe the product in at least ${MIN_DESCRIPTION_LENGTH} characters.`;
    }
    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  }

  function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!validate()) return;

    onSubmit({
      product_name: productName.trim(),
      product_description: productDescription.trim(),
      campaign_objective: objective,
      target_audience: targetAudience.trim() || null,
      campaign_duration_days: durationDays ? Number(durationDays) : null,
      brand_tone: brandTone.trim() || null,
      additional_notes: additionalNotes.trim() || null,
    });
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid gap-6 sm:grid-cols-2">
        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="product_name">Product name</Label>
          <Input
            id="product_name"
            value={productName}
            onChange={(event) => setProductName(event.target.value)}
            placeholder="e.g. Solar Backpack"
            maxLength={120}
            disabled={isSubmitting}
          />
          {errors.product_name && <p className="text-sm text-destructive">{errors.product_name}</p>}
        </div>

        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="product_description">Product description</Label>
          <Textarea
            id="product_description"
            value={productDescription}
            onChange={(event) => setProductDescription(event.target.value)}
            placeholder="What is it, who is it for, what problem does it solve?"
            maxLength={2000}
            rows={4}
            disabled={isSubmitting}
          />
          {errors.product_description && (
            <p className="text-sm text-destructive">{errors.product_description}</p>
          )}
        </div>

        <div className="space-y-2">
          <Label htmlFor="objective">Campaign objective</Label>
          <Select value={objective} onValueChange={(value) => setObjective(value as CampaignObjective)}>
            <SelectTrigger id="objective">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {CAMPAIGN_OBJECTIVES.map((option) => (
                <SelectItem key={option.value} value={option.value}>
                  {option.label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-2">
          <Label htmlFor="duration">Campaign duration (days, optional)</Label>
          <Input
            id="duration"
            type="number"
            min={1}
            max={365}
            value={durationDays}
            onChange={(event) => setDurationDays(event.target.value)}
            placeholder="e.g. 14"
            disabled={isSubmitting}
          />
        </div>

        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="target_audience">Target audience (optional)</Label>
          <Input
            id="target_audience"
            value={targetAudience}
            onChange={(event) => setTargetAudience(event.target.value)}
            placeholder="Leave blank to let Market Intelligence infer it from research"
            maxLength={500}
            disabled={isSubmitting}
          />
        </div>

        <div className="space-y-2">
          <Label htmlFor="brand_tone">Brand tone (optional)</Label>
          <Input
            id="brand_tone"
            value={brandTone}
            onChange={(event) => setBrandTone(event.target.value)}
            placeholder="e.g. playful and bold"
            maxLength={200}
            disabled={isSubmitting}
          />
        </div>

        <div className="space-y-2 sm:col-span-2">
          <Label htmlFor="notes">Additional notes (optional)</Label>
          <Textarea
            id="notes"
            value={additionalNotes}
            onChange={(event) => setAdditionalNotes(event.target.value)}
            placeholder="Anything else the agents should take into account"
            maxLength={1000}
            rows={3}
            disabled={isSubmitting}
          />
        </div>
      </div>

      <Button type="submit" size="lg" disabled={isSubmitting} className="w-full sm:w-auto">
        {isSubmitting ? "Generating campaign..." : "Generate campaign"}
      </Button>
    </form>
  );
}
