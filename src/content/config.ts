import { defineCollection, z } from 'astro:content';

// Single docs collection (deduplicated). Add fields as needed.
const docs = defineCollection({
  schema: z.object({
    title: z.string(),
    group: z.string().optional(),
    order: z.number().optional(),
    status: z.enum(['stable','partial','planned']).optional(),
    description: z.string().optional()
  })
});

export const collections = { docs };