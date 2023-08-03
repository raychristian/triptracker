FROM google/cloud-sdk:341.0.0-alpine

COPY ./run.sh /scripts/run.sh
RUN chmod +x /scripts/*

ENV PATH="/scripts:$PATH"

RUN apk add --update --no-cache openjdk8-jre && \
	gcloud components install cloud-datastore-emulator beta --quiet

CMD ["run.sh"]
