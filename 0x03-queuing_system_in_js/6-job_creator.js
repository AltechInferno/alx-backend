#!/usr/bin/yarn dev
import { createQueue } from 'kue';

const queue = createQueue({name: 'push_notification_code'});

const new_job = queue.create('push_notification_code', {
  phoneNumber: '23350000000',
  message: 'Account registered',
});

new_job
  .on('enqueue', () => {
    console.log('Notification job created:', new_job.id);
  })
  .on('complete', () => {
    console.log('Notification job completed');
  })
  .on('failed attempt', () => {
    console.log('Notification job failed');
  });
new_job.save();
