"""Configuration management for Conversation Analyzer."""

import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
import yaml


@dataclass
class OllamaConfig:
    """Ollama service configuration."""

    host: str = "http://localhost:11434"
    extraction_model: str = "nuextract"
    analysis_model: str = "llama3.1:8b"
    temperature: float = 0.1
    max_tokens: int = 2048
    timeout: int = 60


@dataclass
class ExtractionConfig:
    """Extraction configuration."""

    prompt_version: str = "v1.0"
    confidence_threshold: float = 0.5
    batch_size: int = 10
    chunk_size: int = 1800


@dataclass
class DeduplicationConfig:
    """Deduplication configuration."""

    enabled: bool = True
    similarity_threshold: float = 0.85
    embedding_model: str = "all-MiniLM-L6-v2"


@dataclass
class PriorityScoringConfig:
    """Priority scoring configuration."""

    urgency_keywords: List[str] = field(
        default_factory=lambda: ["urgent", "critical", "asap", "immediately", "blocker"]
    )
    impact_keywords: List[str] = field(
        default_factory=lambda: ["breaks", "blocks", "prevents", "security", "data loss"]
    )
    base_score: float = 0.5


@dataclass
class EntityLinkingConfig:
    """Entity linking configuration."""

    enabled: bool = True
    min_entities_shared: int = 1


@dataclass
class IntelligenceConfig:
    """Intelligence features configuration."""

    deduplication: DeduplicationConfig = field(default_factory=DeduplicationConfig)
    priority_scoring: PriorityScoringConfig = field(default_factory=PriorityScoringConfig)
    entity_linking: EntityLinkingConfig = field(default_factory=EntityLinkingConfig)


@dataclass
class DatabaseConfig:
    """Database configuration."""

    path: str = "data/database/analyzer.db"
    backup_enabled: bool = True
    backup_interval: int = 86400  # seconds


@dataclass
class ReportingConfig:
    """Reporting configuration."""

    output_dir: str = "data/reports"
    formats: List[str] = field(default_factory=lambda: ["markdown", "json"])
    group_by: str = "type"
    include_duplicates: bool = False


@dataclass
class LoggingConfig:
    """Logging configuration."""

    level: str = "INFO"
    file: str = "data/logs/analyzer.log"
    console: bool = True


@dataclass
class SourcesConfig:
    """Sources configuration."""

    conversations: List[str] = field(
        default_factory=lambda: ["data/conversations/**/*.md", "data/conversations/**/*.json"]
    )
    code: List[str] = field(default_factory=lambda: ["**/*.py", "**/*.js", "**/*.ts"])
    documents: List[str] = field(
        default_factory=lambda: ["**/TODO.md", "**/README.md", "**/NOTES.md"]
    )
    git_enabled: bool = False
    git_branch: str = "main"
    git_since: str = "30 days ago"


@dataclass
class Config:
    """Main configuration class."""

    ollama: OllamaConfig = field(default_factory=OllamaConfig)
    extraction: ExtractionConfig = field(default_factory=ExtractionConfig)
    intelligence: IntelligenceConfig = field(default_factory=IntelligenceConfig)
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    reporting: ReportingConfig = field(default_factory=ReportingConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    sources: SourcesConfig = field(default_factory=SourcesConfig)

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "Config":
        """Load configuration from YAML file."""
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f)

        config = cls()

        if not data:
            return config

        # Parse Ollama config
        if "ollama" in data:
            config.ollama = OllamaConfig(**data["ollama"])

        # Parse Extraction config
        if "extraction" in data:
            config.extraction = ExtractionConfig(**data["extraction"])

        # Parse Intelligence config
        if "intelligence" in data:
            intel_data = data["intelligence"]
            dedup = DeduplicationConfig(**intel_data.get("deduplication", {}))
            scoring = PriorityScoringConfig(**intel_data.get("priority_scoring", {}))
            linking = EntityLinkingConfig(**intel_data.get("entity_linking", {}))
            config.intelligence = IntelligenceConfig(
                deduplication=dedup, priority_scoring=scoring, entity_linking=linking
            )

        # Parse Database config
        if "database" in data:
            config.database = DatabaseConfig(**data["database"])

        # Parse Reporting config
        if "reporting" in data:
            config.reporting = ReportingConfig(**data["reporting"])

        # Parse Logging config
        if "logging" in data:
            config.logging = LoggingConfig(**data["logging"])

        # Parse Sources config
        if "sources" in data:
            sources_data = data["sources"]
            git_data = sources_data.get("git", {})
            config.sources = SourcesConfig(
                conversations=sources_data.get("conversations", config.sources.conversations),
                code=sources_data.get("code", config.sources.code),
                documents=sources_data.get("documents", config.sources.documents),
                git_enabled=git_data.get("enabled", False),
                git_branch=git_data.get("branch", "main"),
                git_since=git_data.get("since", "30 days ago"),
            )

        return config

    @classmethod
    def from_env(cls) -> "Config":
        """Load configuration from environment variables."""
        config = cls()

        # Ollama from env
        if host := os.getenv("OLLAMA_HOST"):
            config.ollama.host = host
        if model := os.getenv("OLLAMA_MODEL"):
            config.ollama.extraction_model = model

        # Database from env
        if db_path := os.getenv("DATABASE_PATH"):
            config.database.path = db_path

        # Logging from env
        if log_level := os.getenv("LOG_LEVEL"):
            config.logging.level = log_level
        if log_file := os.getenv("LOG_FILE"):
            config.logging.file = log_file

        return config

    @classmethod
    def load(cls, yaml_path: Optional[str] = None) -> "Config":
        """Load configuration from YAML and override with env vars."""
        # Start with defaults
        config = cls()

        # Load from YAML if provided
        if yaml_path and Path(yaml_path).exists():
            config = cls.from_yaml(yaml_path)
        elif Path("config.yaml").exists():
            config = cls.from_yaml("config.yaml")

        # Override with environment variables
        env_config = cls.from_env()
        config.ollama.host = env_config.ollama.host or config.ollama.host
        config.ollama.extraction_model = (
            env_config.ollama.extraction_model or config.ollama.extraction_model
        )
        config.database.path = env_config.database.path or config.database.path
        config.logging.level = env_config.logging.level or config.logging.level
        config.logging.file = env_config.logging.file or config.logging.file

        return config

    def ensure_directories(self):
        """Ensure all required directories exist."""
        dirs_to_create = [
            Path(self.database.path).parent,
            Path(self.logging.file).parent,
            Path(self.reporting.output_dir),
        ]

        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)
