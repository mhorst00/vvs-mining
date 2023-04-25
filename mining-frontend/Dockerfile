####################################################################################################
## Builder
####################################################################################################
FROM node:current-alpine AS builder

# Create appuser
ENV USER=backend
ENV UID=10001

RUN adduser \
  --disabled-password \
  --gecos "" \
  --home "/nonexistent" \
  --shell "/sbin/nologin" \
  --no-create-home \
  --uid "${UID}" \
  "${USER}"

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
RUN npm run build

####################################################################################################
## Final image
####################################################################################################
FROM node:current-alpine

# Import from builder.
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

WORKDIR /app

# Copy our build
COPY --from=builder /app/build .

# Copy package.json to make app look like a module
COPY package.json .

# Espose the app port
EXPOSE 3000

# Use an unprivileged user.
USER backend:backend

ENV PROTOCOL_HEADER=x-forwarded-proto
ENV HOST_HEADER=x-forwarded-host

CMD [ "node", "index.js" ]
