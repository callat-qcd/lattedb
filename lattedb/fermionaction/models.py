from django.db import models

from espressodb.base.models import Base


class FermionAction(Base):
    r"""
    Base table for application.
    All types of fermion actions are listed here.
    If applicable, consistency is enforced in check_consistency under each table that references $\texttt{fermionaction.fermionaction}$.
    """


class Hisq(FermionAction):
    """
    """

    quark_mass = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Input quark mass",
    )
    quark_tag = models.TextField(
        blank=False, null=False, help_text="Type of quark"
    )

    naik = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Coefficient of Naik term. If Naik term is not included, explicitly set to 0",
    )
    linksmear = models.ForeignKey(
        "linksmear.LinkSmear",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to additional gauge $\texttt{linksmear}$ outside of Monte Carlo.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quark_mass", "quark_tag", "naik", "linksmear"],
                name="unique_fermionaction_hisq",
            )
        ]

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["quark_tag"] not in [
            "light",
            "up",
            "down",
            "strange",
            "charm",
            "bottom",
        ]:
            raise ValueError(
                """Requires quark_tag to be in ["light", "up", "down", "strange", "charm", "bottom"]."""
            )


class MobiusDW(FermionAction):
    """
    """

    quark_mass = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Input quark mass",
    )
    quark_tag = models.TextField(
        blank=False, null=False, help_text="Type of quark"
    )

    l5 = models.PositiveSmallIntegerField(
        help_text="Length of 5th dimension"
    )
    m5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="5th dimensional mass",
    )
    b5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Mobius kernel parameter [a5 = b5 - c5, alpha5 * a5 = b5 + c5]",
    )
    c5 = models.DecimalField(
        max_digits=10,
        decimal_places=6,
        null=False,
        help_text="Mobius kernal perameter",
    )
    linksmear = models.ForeignKey(
        "linksmear.LinkSmear",
        on_delete=models.CASCADE,
        help_text=r"Foreign Key pointing to additional gauge $\texttt{linksmear}$ outside of Monte Carlo.",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["quark_mass", "quark_tag", "l5", "m5", "b5", "c5", "linksmear"],
                name="unique_fermionaction_mobiusdw",
            )
        ]

    @property
    def alpha5(self) -> float:
        """c5 + b5
        """
        return self.c5 + self.b5

    @classmethod
    def check_consistency(cls, data: Dict[str, Any]):
        if data["quark_tag"] not in [
            "light",
            "up",
            "down",
            "strange",
            "charm",
            "bottom",
        ]:
            raise ValueError(
                """Requires quark_tag to be in ["light", "up", "down", "strange", "charm", "bottom"]."""
            )
