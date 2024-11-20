package morkato.api.dto.validation;

import jakarta.validation.Constraint;
import jakarta.validation.Payload;
import jakarta.validation.constraints.Pattern;
import org.hibernate.validator.constraints.Length;

import java.lang.annotation.*;

@Length(min = 2, max = 128)
@Pattern(regexp = "^[^\\s][^:]{1,127}$")
@Target({ ElementType.FIELD, ElementType.METHOD, ElementType.PARAMETER, ElementType.ANNOTATION_TYPE })
@Retention(RetentionPolicy.RUNTIME) 
@Documented
@Constraint(validatedBy = {})
public @interface ResumeDescriptionSchema {
  String message() default "This resume-description is invalid!";
  Class<?>[] groups() default {};
  Class<? extends Payload>[] payload() default {};
}